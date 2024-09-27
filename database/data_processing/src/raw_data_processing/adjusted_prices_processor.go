package raw_data_processing

import (
	"encoding/csv"
	"fmt"
	"main/src/models"
	"main/src/utils"
	"path/filepath"
	"sync"
)

// AdjustedPricesProcessor processes adjusted prices and stores them in multiple smaller CSV files (e.g., 50,000 rows per file).
func AdjustedPricesProcessor(input models.ProcessorInput) error {
	var wg sync.WaitGroup
	results := make(chan models.DataFrame, len(input.Symbols)) // Channel to collect processed data
	sem := make(chan struct{}, 10)                             // Semaphore to limit concurrent goroutines

	// Iterate over symbols in the Symbols map
	for symbol := range input.Symbols {
		wg.Add(1)
		go func(symbol string) {
			defer wg.Done()
			sem <- struct{}{}        // Acquire semaphore
			defer func() { <-sem }() // Release semaphore

			df, err := processSingleAdjustedPriceCSV(input.InputPath, symbol)
			if err != nil {
				fmt.Println("Error processing CSV:", err)
				return
			}
			results <- df
		}(symbol)
	}

	// Wait for all goroutines to finish
	go func() {
		wg.Wait()
		close(results)
	}()

	// Collect results and write them in chunks of 50,000 rows
	rowLimit := 50000
	batchIndex := 0

	var currentBatch []models.CSVRecord
	for df := range results {
		currentBatch = append(currentBatch, df.Records...)

		// Once we've reached 50,000 rows, write the batch to a new CSV file
		for len(currentBatch) >= rowLimit {
			batch := currentBatch[:rowLimit]
			currentBatch = currentBatch[rowLimit:]

			outputPath := filepath.Join(input.OutputPath, fmt.Sprintf("%s_part_%d.csv", input.Name, batchIndex))
			err := writeBatchToCSV(outputPath, input.NewColumnsNames, batch)
			if err != nil {
				return err
			}
			batchIndex++
		}
	}

	// Write any remaining records that didn't fill up to 50,000 rows
	if len(currentBatch) > 0 {
		outputPath := filepath.Join(input.OutputPath, fmt.Sprintf("%s_part_%d.csv", input.Name, batchIndex))
		err := writeBatchToCSV(outputPath, input.NewColumnsNames, currentBatch)
		if err != nil {
			return err
		}
	}

	fmt.Println(input.Name + " generation complete. Data split into multiple files.")
	return nil
}

// processSingleCSV reads and processes a single CSV file.
func processSingleAdjustedPriceCSV(path string, symbol string) (models.DataFrame, error) {
	file, err := utils.OpenCSVFile(path, symbol)
	if err != nil {
		return models.DataFrame{}, err
	}
	defer file.Close()

	reader := csv.NewReader(file)

	priceIndex, err := readHeaderAndFindColumn(reader, "price")
	if err != nil {
		return models.DataFrame{}, err
	}

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
				break
			}
			return nil, fmt.Errorf("failed to read row: %w", err)
		}

		if row[priceIndex] == "" {
			newRow := models.CSVRecord{
				Values: append(row, symbol),
			}
			processedRecords = append(processedRecords, newRow)
			continue
		}

		price, err := parseAndRoundFloat(row, priceIndex, 3)
		if err != nil {
			return nil, fmt.Errorf("error parsing price: %w", err)
		}
		row[priceIndex] = price

		newRow := models.CSVRecord{
			Values: append(row, symbol),
		}
		processedRecords = append(processedRecords, newRow)
	}

	return processedRecords, nil
}
