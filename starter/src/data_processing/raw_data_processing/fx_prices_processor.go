package raw_data_processing

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
	"starter/src"
	"strings"
	"sync"
)

func FXPricesProcessor(input src.ProcessorInput) error {
	fmt.Printf("Generating Fx prices\n")

	var wg sync.WaitGroup
	results := make(chan src.DataFrame) // Channel to collect processed data
	sem := make(chan struct{}, 10)      // Semaphore to limit concurrent goroutines

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
			df, err := processSingleFXPriceCSV(input.Path, src.CSVRecord{Values: []string{fileName}})
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
	err = writeMergedCSV(outputPath, input.NewColumnsNames, mergedData)
	if err != nil {
		return err
	}

	return nil
}

// processSingleFXPriceCSV reads and processes a single CSV file without changing the header (header will be added during the merge).
func processSingleFXPriceCSV(path string, symbol src.CSVRecord) (src.DataFrame, error) {
	// Step 1: Open the CSV file
	file, err := openCSVFile(path, symbol.Values[0])
	if err != nil {
		return src.DataFrame{}, err
	}
	defer file.Close()

	reader := csv.NewReader(file)

	// Step 2: Read the header and find the price column index
	priceIndex, err := readHeaderAndFindColumn(reader, "PRICE")
	if err != nil {
		return src.DataFrame{}, err
	}

	// Step 3: Process all rows
	processedRecords, err := processFxPricesRows(reader, priceIndex, symbol)
	if err != nil {
		return src.DataFrame{}, err
	}

	return src.DataFrame{
		SymbolName: symbol.Values[0],
		Records:    processedRecords,
	}, nil
}

// processFxPricesRows processes each row, parses and rounds the price, and appends the symbol.
func processFxPricesRows(reader *csv.Reader, priceIndex int, symbol src.CSVRecord) ([]src.CSVRecord, error) {
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
