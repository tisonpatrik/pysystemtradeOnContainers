package raw_data_processing

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
	"starter/src"
	"sync"
)

func RollCalendarsProcessor(input src.ProcessorInput) error {
	fmt.Printf("Generating Roll Calendars\n")

	var wg sync.WaitGroup
	results := make(chan src.DataFrame, len(input.Symbols)) // Channel to collect processed data
	sem := make(chan struct{}, 10)                          // Semaphore to limit concurrent goroutines

	for _, symbol := range input.Symbols {
		wg.Add(1)
		go func(symbol src.CSVRecord) {
			defer wg.Done()
			sem <- struct{}{}        // Acquire semaphore to limit concurrent goroutines
			defer func() { <-sem }() // Release semaphore after processing

			// Now passing just the file name without extension
			df, err := processSingleRollCalendarsCSV(input.Path, symbol)
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

	return nil
}

// process single RollCalendarCSV reads and processes a single CSV file without changing the header (header will be added during the merge).
func processSingleRollCalendarsCSV(path string, symbol src.CSVRecord) (src.DataFrame, error) {
	// Step 1: Open the CSV file
	file, err := openCSVFile(path, symbol.Values[0])
	if err != nil {
		return src.DataFrame{}, err
	}
	defer file.Close()

	reader := csv.NewReader(file)

	// Step 3: Process all rows
	processedRecords, err := processRollCalendarsRows(reader, symbol)
	if err != nil {
		return src.DataFrame{}, err
	}

	return src.DataFrame{
		SymbolName: symbol.Values[0],
		Records:    processedRecords,
	}, nil
}

// process RollCalendars Rows processes each row and appends the symbol.
func processRollCalendarsRows(reader *csv.Reader, symbol src.CSVRecord) ([]src.CSVRecord, error) {
	var processedRecords []src.CSVRecord

	// Read the header to determine the correct number of columns
	header, err := reader.Read()
	if err != nil {
		return nil, fmt.Errorf("failed to read header: %w", err)
	}
	columnCount := len(header) // Get the number of columns from the header

	for {
		row, err := reader.Read()
		if err != nil {
			if err.Error() == "EOF" {
				break // End of file reached
			}
			return nil, fmt.Errorf("failed to read row: %w", err)
		}

		// Truncate or adjust the row to fit the number of columns in the header
		if len(row) > columnCount {
			row = row[:columnCount] // Keep only values up to the column count
		}

		// Append the symbol to the row
		newRow := src.CSVRecord{
			Values: append(row, symbol.Values[0]),
		}
		processedRecords = append(processedRecords, newRow)
	}

	return processedRecords, nil
}
