package raw_data_processing

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
	"starter/src"
	"sync"
)

// AdjustedPricesProcessor processes adjusted prices based on CSV files in the directory and symbols.
func AdjustedPricesProcessor(input src.ProcessorInput) error {
	var wg sync.WaitGroup
	results := make(chan src.DataFrame, len(input.Symbols)) // Channel to collect processed data
	sem := make(chan struct{}, 10)                          // Semaphore to limit concurrent goroutines

	for _, symbol := range input.Symbols {
		wg.Add(1)
		go func(symbol src.CSVRecord) {
			defer wg.Done()
			sem <- struct{}{}        // Acquire semaphore to limit concurrent goroutines
			defer func() { <-sem }() // Release semaphore after processing

			df, err := processSingleAdjustedPriceCSV(input.Path, symbol)
			if err != nil {
				fmt.Println("Error processing CSV:", err)
				return
			}
			results <- df
		}(symbol) // Pass symbol as argument here to avoid closure issue
	}

	// Wait for all goroutines to finish
	go func() {
		wg.Wait()
		close(results)
	}()

	// Collect results and merge them
	var mergedData []src.CSVRecord
	for df := range results {
		mergedData = append(mergedData, df.Records...)
	}

	// Ensure the directory exists before writing the final merged CSV
	outputDir := filepath.Join("data", "raw_data")
	if err := os.MkdirAll(outputDir, os.ModePerm); err != nil {
		return fmt.Errorf("failed to create directory: %w", err)
	}

	// Write the final merged CSV to the specified directory and with the specified name
	outputPath := filepath.Join(outputDir, input.Name)
	err := writeMergedCSV(outputPath, input.NewColumnsNames, mergedData)
	if err != nil {
		return err
	}
	fmt.Println(input.Name + " generation complete. Final records saved to CSV.")
	return nil
}

// processSingleCSV reads and processes a single CSV file without changing the header (header will be added during the merge).
func processSingleAdjustedPriceCSV(path string, symbol src.CSVRecord) (src.DataFrame, error) {
	// Step 1: Open the CSV file
	file, err := openCSVFile(path, symbol.Values[0])
	if err != nil {
		return src.DataFrame{}, err
	}
	defer file.Close()

	reader := csv.NewReader(file)

	// Step 2: Read the header and find the price column index
	priceIndex, err := readHeaderAndFindColumn(reader, "price")
	if err != nil {
		return src.DataFrame{}, err
	}

	// Step 3: Process all rows
	processedRecords, err := processAdjustedPricesRows(reader, priceIndex, symbol)
	if err != nil {
		return src.DataFrame{}, err
	}

	return src.DataFrame{
		SymbolName: symbol.Values[0],
		Records:    processedRecords,
	}, nil
}

// processAdjustedPricesRows processes each row, parses and rounds the price, and appends the symbol.
func processAdjustedPricesRows(reader *csv.Reader, priceIndex int, symbol src.CSVRecord) ([]src.CSVRecord, error) {
	var processedRecords []src.CSVRecord

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
			newRow := src.CSVRecord{
				Values: append(row, symbol.Values[0]),
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
		newRow := src.CSVRecord{
			Values: append(row, symbol.Values[0]),
		}
		processedRecords = append(processedRecords, newRow)
	}

	return processedRecords, nil
}
