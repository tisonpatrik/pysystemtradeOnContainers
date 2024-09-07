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

			df, err := processSingleCSV(input.Path, symbol, input.NewColumnsNames)
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

	// Write the final merged CSV
	err := writeMergedCSV(filepath.Join(input.Path, input.Name), input.NewColumnsNames, mergedData)
	if err != nil {
		return err
	}

	return nil
}
func processSingleCSV(path string, symbol src.CSVRecord, newColumnsNames []string) (src.DataFrame, error) {
	filePath := filepath.Join(path, symbol.Values[0]+".csv")
	file, err := os.Open(filePath)
	if err != nil {
		return src.DataFrame{}, err
	}
	defer file.Close()

	reader := csv.NewReader(file)

	// Stream process the CSV file row by row
	var processedRecords []src.CSVRecord
	for {
		row, err := reader.Read()
		if err != nil {
			if err.Error() == "EOF" {
				break // End of file reached
			}
			return src.DataFrame{}, err
		}

		newRow := src.CSVRecord{
			Columns: newColumnsNames,
			Values:  append(row, symbol.Values[0]),
		}
		processedRecords = append(processedRecords, newRow)
	}

	return src.DataFrame{
		SymbolName: symbol.Values[0],
		Records:    processedRecords,
	}, nil
}

// writeMergedCSV writes the final merged CSV file.
func writeMergedCSV(filePath string, columns []string, records []src.CSVRecord) error {
	file, err := os.Create(filePath)
	if err != nil {
		return err
	}
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()

	// Write the header
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
