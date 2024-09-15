package raw_data_processing

import (
	"encoding/csv"
	"fmt"
	"main/src/models"
	"main/src/utils"
	"os"
	"path/filepath"
	"strings"
	"sync"
)

func FXPricesProcessor(input models.ProcessorInput) error {
	var wg sync.WaitGroup
	results := make(chan models.DataFrame) // Channel to collect processed data
	sem := make(chan struct{}, 10)         // Semaphore to limit concurrent goroutines

	// Get all CSV files from the input.Path directory (which should be data/temp/fx_prices_csv)
	files, err := filepath.Glob(filepath.Join(input.Path, "*.csv"))
	if err != nil {
		return fmt.Errorf("failed to read files: %w", err)
	}

	// Process each CSV file
	for _, file := range files {
		// Extract the base file name without extension
		fileName := strings.TrimSuffix(filepath.Base(file), ".csv")

		wg.Add(1)
		go func(fileName string) {
			defer wg.Done()
			sem <- struct{}{}        // Acquire semaphore to limit concurrent goroutines
			defer func() { <-sem }() // Release semaphore after processing

			// Now passing just the file name without extension
			df, err := processSingleFXPriceCSV(input.Path, models.CSVRecord{Values: []string{fileName}})
			if err != nil {
				fmt.Println("Error processing CSV:", err)
				return
			}
			results <- df
		}(fileName) // Pass fileName to avoid closure issue
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

	// Ensure the directory exists before writing the final merged CSV
	outputDir := filepath.Join("database/data", "raw_data")
	if err := os.MkdirAll(outputDir, os.ModePerm); err != nil {
		return fmt.Errorf("failed to create directory: %w", err)
	}

	// Write the final merged CSV to the specified directory and with the specified name
	outputPath := filepath.Join(outputDir, input.Name)
	columns := append(input.NewColumnsNames, "symbol")
	err = utils.WriteCSVFile(outputPath, columns, mergedData)
	if err != nil {
		return err
	}
	fmt.Println(input.Name + " generation complete. Final records saved to CSV.")
	return nil
}

// processSingleFXPriceCSV reads and processes a single CSV file without changing the header (header will be added during the merge).
func processSingleFXPriceCSV(path string, symbol models.CSVRecord) (models.DataFrame, error) {
	// Step 1: Open the CSV file
	file, err := utils.OpenCSVFile(path, symbol.Values[0])
	if err != nil {
		return models.DataFrame{}, err
	}
	defer file.Close()

	reader := csv.NewReader(file)

	// Step 2: Read the header and find the price column index
	priceIndex, err := readHeaderAndFindColumn(reader, "PRICE")
	if err != nil {
		return models.DataFrame{}, err
	}

	// Step 3: Process all rows
	processedRecords, err := processFxPricesRows(reader, priceIndex, symbol)
	if err != nil {
		return models.DataFrame{}, err
	}

	return models.DataFrame{
		SymbolName: symbol.Values[0],
		Records:    processedRecords,
	}, nil
}

// processFxPricesRows processes each row, parses and rounds the price, and appends the symbol.
func processFxPricesRows(reader *csv.Reader, priceIndex int, symbol models.CSVRecord) ([]models.CSVRecord, error) {
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
		newRow := models.CSVRecord{
			Values: append(row, symbol.Values[0]),
		}
		processedRecords = append(processedRecords, newRow)
	}

	return processedRecords, nil
}