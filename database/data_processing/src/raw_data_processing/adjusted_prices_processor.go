package raw_data_processing

import (
	"encoding/csv"
	"fmt"
	"main/src/models"
	"main/src/utils"
	"os"
	"path/filepath"
	"sync"
)

// AdjustedPricesProcessor processes adjusted prices based on CSV files in the directory and symbols.
func AdjustedPricesProcessor(input models.ProcessorInput) error {
	var wg sync.WaitGroup
	results := make(chan models.DataFrame, len(input.Symbols)) // Channel to collect processed data
	sem := make(chan struct{}, 10)                             // Semaphore to limit concurrent goroutines

	// Iterate over symbols in the Symbols map
	for symbol := range input.Symbols {
		wg.Add(1)
		go func(symbol string) { // symbol is now a string, not models.CSVRecord
			defer wg.Done()
			sem <- struct{}{}        // Acquire semaphore to limit concurrent goroutines
			defer func() { <-sem }() // Release semaphore after processing

			df, err := processSingleAdjustedPriceCSV(input.InputPath, symbol)
			if err != nil {
				fmt.Println("Error processing CSV:", err)
				return
			}
			results <- df
		}(symbol) // Pass symbol (string) as argument to avoid closure issue
	}

	// Wait for all goroutines to finish
	go func() {
		wg.Wait()
		close(results)
	}()

	// Collect results and merge them
	var mergedData []models.CSVRecord
	for df := range results {
		mergedData = append(mergedData, df.Records...)
	}

	// Write the final merged CSV to the specified directory and with the specified name
	outputPath := filepath.Join(input.OutputPath, input.Name)
	columns := append(input.NewColumnsNames, "symbol")

	// Ensure the output directory exists
	err := os.MkdirAll(input.OutputPath, os.ModePerm)
	if err != nil {
		return fmt.Errorf("error creating output directory %s: %w", input.OutputPath, err)
	}

	err = utils.WriteCSVFile(outputPath, columns, mergedData)
	if err != nil {
		return err
	}
	fmt.Println(input.Name + " generation complete. Final records saved to CSV.")
	return nil
}

// processSingleCSV reads and processes a single CSV file without changing the header (header will be added during the merge).
func processSingleAdjustedPriceCSV(path string, symbol string) (models.DataFrame, error) {
	// Step 1: Open the CSV file
	file, err := utils.OpenCSVFile(path, symbol)
	if err != nil {
		return models.DataFrame{}, err
	}
	defer file.Close()

	reader := csv.NewReader(file)

	// Step 2: Read the header and find the price column index
	priceIndex, err := readHeaderAndFindColumn(reader, "price")
	if err != nil {
		return models.DataFrame{}, err
	}

	// Step 3: Process all rows
	processedRecords, err := processAdjustedPricesRows(reader, priceIndex, symbol)
	if err != nil {
		return models.DataFrame{}, err
	}

	return models.DataFrame{
		SymbolName: symbol,
		Records:    processedRecords,
	}, nil
}

// processAdjustedPricesRows processes each row, parses and rounds the price, and appends the symbol.
func processAdjustedPricesRows(reader *csv.Reader, priceIndex int, symbol string) ([]models.CSVRecord, error) {
	var processedRecords []models.CSVRecord

	for {
		row, err := reader.Read()
		if err != nil {
			if err.Error() == "EOF" {
				break // End of file reached
			}
			return nil, fmt.Errorf("failed to read row: %w", err)
		}

		// Check if the price field is empty
		if row[priceIndex] == "" {
			// Add the row to the list without processing the price
			newRow := models.CSVRecord{
				Values: append(row, symbol),
			}
			processedRecords = append(processedRecords, newRow)
			continue
		}

		// Parse and round the price if it's not empty
		price, err := parseAndRoundFloat(row, priceIndex, 3)
		if err != nil {
			return nil, fmt.Errorf("error parsing price: %w", err)
		}
		row[priceIndex] = price

		// Append the symbol to the row
		newRow := models.CSVRecord{
			Values: append(row, symbol),
		}
		processedRecords = append(processedRecords, newRow)
	}

	return processedRecords, nil
}
