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

func RollCalendarsProcessor(input models.ProcessorInput) error {
	var wg sync.WaitGroup
	results := make(chan models.DataFrame, len(input.Symbols)) // Channel to collect processed data
	sem := make(chan struct{}, 10)                             // Semaphore to limit concurrent goroutines

	for symbol := range input.Symbols {
		wg.Add(1)
		go func(symbol string) {
			defer wg.Done()
			sem <- struct{}{}        // Acquire semaphore to limit concurrent goroutines
			defer func() { <-sem }() // Release semaphore after processing

			// Now passing just the file name without extension
			df, err := processSingleRollCalendarsCSV(input.InputPath, symbol)
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

// process single RollCalendarCSV reads and processes a single CSV file without changing the header (header will be added during the merge).
func processSingleRollCalendarsCSV(path string, symbol string) (models.DataFrame, error) {
	// Step 1: Open the CSV file
	file, err := utils.OpenCSVFile(path, symbol)
	if err != nil {
		return models.DataFrame{}, err
	}
	defer file.Close()

	reader := csv.NewReader(file)

	// Step 3: Process all rows
	processedRecords, err := processRollCalendarsRows(reader, symbol)
	if err != nil {
		return models.DataFrame{}, err
	}

	return models.DataFrame{
		SymbolName: symbol,
		Records:    processedRecords,
	}, nil
}

// processRollCalendarsRows processes each row and appends the symbol, removing any extra columns beyond the expected count.
func processRollCalendarsRows(reader *csv.Reader, symbol string) ([]models.CSVRecord, error) {
	var processedRecords []models.CSVRecord

	// Read the header to determine the correct number of columns
	header, err := reader.Read()
	if err != nil {
		return nil, fmt.Errorf("failed to read header: %w", err)
	}
	columnCount := len(header)

	// We expect 4 columns based on the structure (DATE_TIME, current_contract, next_contract, carry_contract)
	expectedColumnCount := 4

	for {
		row, err := reader.Read()
		if err != nil {
			if err.Error() == "EOF" {
				break // End of file reached
			}
			return nil, fmt.Errorf("failed to read row: %w", err)
		}

		// If there are more than 4 columns, truncate the row to the first 4 columns
		if columnCount > expectedColumnCount {
			row = row[:expectedColumnCount] // Remove any extra columns
		}

		// Append the symbol as the 5th column
		newRow := models.CSVRecord{
			Values: append(row, symbol),
		}
		processedRecords = append(processedRecords, newRow)
	}

	return processedRecords, nil
}
