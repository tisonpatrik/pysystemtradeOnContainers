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

func MultiplePricesProcessor(input models.ProcessorInput) error {
	var wg sync.WaitGroup
	results := make(chan models.DataFrame, len(input.Symbols)) // Channel to collect processed data
	sem := make(chan struct{}, 10)                             // Semaphore to limit concurrent goroutines

	for symbol := range input.Symbols {
		wg.Add(1)
		go func(symbol string) {
			defer wg.Done()
			sem <- struct{}{}        // Acquire semaphore to limit concurrent goroutines
			defer func() { <-sem }() // Release semaphore after processing

			df, err := processSingleMultiplePriceCSV(input.Path, symbol)
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

	// Ensure the directory exists before writing the final merged CSV
	outputDir := filepath.Join("database/data", "raw_data")
	if err := os.MkdirAll(outputDir, os.ModePerm); err != nil {
		return fmt.Errorf("failed to create directory: %w", err)
	}
	// Write the final merged CSV to the specified directory and with the specified name
	outputPath := filepath.Join(outputDir, input.Name)
	columns := append(input.NewColumnsNames, "symbol")
	err := utils.WriteCSVFile(outputPath, columns, mergedData)
	if err != nil {
		return err
	}
	fmt.Println(input.Name + " generation complete. Final records saved to CSV.")
	return nil
}

// processSingleMultiplePriceCSV reads and processes a single CSV file, ensuring that the first row is treated as a header.
func processSingleMultiplePriceCSV(path string, symbol string) (models.DataFrame, error) {
	// Step 1: Open the CSV file
	file, err := utils.OpenCSVFile(path, symbol)
	if err != nil {
		return models.DataFrame{}, fmt.Errorf("error opening file: %w", err)
	}
	defer file.Close()

	reader := csv.NewReader(file)

	// Step 2: Read the header and find the required column indices
	header, err := reader.Read()
	if err != nil {
		return models.DataFrame{}, fmt.Errorf("failed to read header: %w", err)
	}

	// Make sure to check if the header row is valid
	if len(header) == 0 {
		return models.DataFrame{}, fmt.Errorf("empty header in CSV")
	}

	// Now find the relevant column indices
	priceIndex, err := findColumnIndex(header, "PRICE")
	if err != nil {
		return models.DataFrame{}, fmt.Errorf("error finding PRICE column: %w", err)
	}

	carryContractIndex, err := findColumnIndex(header, "CARRY_CONTRACT")
	if err != nil {
		return models.DataFrame{}, fmt.Errorf("error finding CARRY_CONTRACT column: %w", err)
	}

	forwardContractIndex, err := findColumnIndex(header, "FORWARD_CONTRACT")
	if err != nil {
		return models.DataFrame{}, fmt.Errorf("error finding FORWARD_CONTRACT column: %w", err)
	}

	priceContractIndex, err := findColumnIndex(header, "PRICE_CONTRACT")
	if err != nil {
		return models.DataFrame{}, fmt.Errorf("error finding PRICE_CONTRACT column: %w", err)
	}

	// Step 3: Process all rows
	processedRecords, err := processMultiplePricesRows(reader, priceIndex, carryContractIndex, forwardContractIndex, priceContractIndex, symbol)
	if err != nil {
		return models.DataFrame{}, fmt.Errorf("error processing rows: %w", err)
	}

	return models.DataFrame{
		SymbolName: symbol,
		Records:    processedRecords,
	}, nil
}

// processMultiplePricesRows processes each row, parses and rounds the price, and appends the symbol.
func processMultiplePricesRows(reader *csv.Reader, priceIndex int, carryContractIndex int, forwardContractIndex int, priceContractIndex int, symbol string) ([]models.CSVRecord, error) {
	var processedRecords []models.CSVRecord

	for {
		row, err := reader.Read()
		if err != nil {
			if err.Error() == "EOF" {
				break // End of file reached
			}
			return nil, fmt.Errorf("failed to read row: %w", err)
		}

		// Check if the price field is empty, but add the row to the list
		if row[priceIndex] != "" {
			// Parse and round the price if it's not empty
			price, err := parseAndRoundFloat(row, priceIndex, 3)
			if err != nil {
				return nil, fmt.Errorf("error parsing price: %w", err)
			}
			row[priceIndex] = price
		}

		// Check if the carry_contract field is empty
		if row[carryContractIndex] != "" {
			// Parse carry_contract as an integer if it's not empty
			carryContract, err := parseAndFormatInt(row, carryContractIndex)
			if err != nil {
				return nil, fmt.Errorf("error parsing carry_contract: %w", err)
			}
			row[carryContractIndex] = carryContract
		}

		// Check if the forward_contract field is empty
		if row[forwardContractIndex] != "" {
			// Parse forward_contract as an integer if it's not empty
			forwardContract, err := parseAndFormatInt(row, forwardContractIndex)
			if err != nil {
				return nil, fmt.Errorf("error parsing forward_contract: %w", err)
			}
			row[forwardContractIndex] = forwardContract
		}

		// Check if the price_contract field is empty
		if row[priceContractIndex] != "" {
			// Parse price_contract as an integer if it's not empty
			priceContract, err := parseAndFormatInt(row, priceContractIndex)
			if err != nil {
				return nil, fmt.Errorf("error parsing price_contract: %w", err)
			}
			row[priceContractIndex] = priceContract
		}

		// Append the symbol to the row
		newRow := models.CSVRecord{
			Values: append(row, symbol),
		}
		processedRecords = append(processedRecords, newRow)
	}

	return processedRecords, nil
}
