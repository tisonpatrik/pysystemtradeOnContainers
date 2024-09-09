package raw_data_processing

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
	"starter/src"
	"strconv"
	"sync"
)

// AdjustedPricesProcessor processes adjusted prices based on CSV files in the directory and symbols.
func AdjustedPricesProcessor(input src.ProcessorInput) error {
	fmt.Printf("Generating metadata for file: %s\n", input.Name)

	var wg sync.WaitGroup
	results := make(chan src.DataFrame, len(input.Symbols)) // Channel to collect processed data
	sem := make(chan struct{}, 10)                          // Semaphore to limit concurrent goroutines

	for _, symbol := range input.Symbols {
		wg.Add(1)
		go func(symbol src.CSVRecord) {
			defer wg.Done()
			sem <- struct{}{}        // Acquire semaphore to limit concurrent goroutines
			defer func() { <-sem }() // Release semaphore after processing

			df, err := processSingleCSV(input.Path, symbol)
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
	outputDir := filepath.Join("data", "adjusted_prices")
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

// processSingleCSV reads and processes a single CSV file without changing the header (header will be added during the merge).
func processSingleCSV(path string, symbol src.CSVRecord) (src.DataFrame, error) {
	filePath := filepath.Join(path, symbol.Values[0]+".csv")
	file, err := os.Open(filePath)
	if err != nil {
		return src.DataFrame{}, err
	}
	defer file.Close()

	reader := csv.NewReader(file)

	// Stream process the CSV file row by row
	var processedRecords []src.CSVRecord
	_, err = reader.Read() // Skip the first row (header) because it will be handled during the merge
	if err != nil {
		return src.DataFrame{}, err
	}

	for {
		row, err := reader.Read()
		if err != nil {
			if err.Error() == "EOF" {
				break // End of file reached
			}
			return src.DataFrame{}, err
		}

		// Skip rows where the price field is empty
		if row[1] == "" {
			continue // Silently skip rows with an empty price field
		}

		// Parse and format the price to 3 decimal places
		price, err := strconv.ParseFloat(row[1], 64)
		if err != nil {
			return src.DataFrame{}, fmt.Errorf("error parsing price: %w", err)
		}
		row[1] = fmt.Sprintf("%.3f", price) // Round to 3 decimal places

		// Process the rows by appending the symbol
		newRow := src.CSVRecord{
			Values: append(row, symbol.Values[0]), // Append symbol value
		}
		processedRecords = append(processedRecords, newRow)
	}

	return src.DataFrame{
		SymbolName: symbol.Values[0],
		Records:    processedRecords,
	}, nil
}

// writeMergedCSV writes the final merged CSV file and adds the header.
func writeMergedCSV(filePath string, columns []string, records []src.CSVRecord) error {
	// Append the "symbol" column to the header
	columns = append(columns, "symbol")
	file, err := os.Create(filePath)
	if err != nil {
		return err
	}
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()

	// Write the header once here
	if err := writer.Write(columns); err != nil {
		return err
	}

	// Write all records
	for _, record := range records {
		if err := writer.Write(record.Values); err != nil {
			return err
		}
	}

	return nil
}
