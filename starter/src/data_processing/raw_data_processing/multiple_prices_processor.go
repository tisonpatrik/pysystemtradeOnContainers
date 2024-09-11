package raw_data_processing

import (
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
	"starter/src"
	"sync"
)

func MultiplePricesProcessor(input src.ProcessorInput) error {
	fmt.Printf("Generating Multiple prices\n")

	var wg sync.WaitGroup
	results := make(chan src.DataFrame, len(input.Symbols)) // Channel to collect processed data
	sem := make(chan struct{}, 10)                          // Semaphore to limit concurrent goroutines

	for _, symbol := range input.Symbols {
		wg.Add(1)
		go func(symbol src.CSVRecord) {
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

// processSingleMultiplePriceCSV reads and processes a single CSV file, ensuring that the first row is treated as a header.
func processSingleMultiplePriceCSV(path string, symbol src.CSVRecord) (src.DataFrame, error) {
	// Step 1: Open the CSV file
	file, err := openCSVFile(path, symbol.Values[0])
	if err != nil {
		return src.DataFrame{}, fmt.Errorf("error opening file: %w", err)
	}
	defer file.Close()

	reader := csv.NewReader(file)

	// Step 2: Read the header and find the required column indices
	header, err := reader.Read()
	if err != nil {
		return src.DataFrame{}, fmt.Errorf("failed to read header: %w", err)
	}

	// Make sure to check if the header row is valid
	if len(header) == 0 {
		return src.DataFrame{}, fmt.Errorf("empty header in CSV")
	}

	// Now find the relevant column indices
	priceIndex, err := findColumnIndex(header, "PRICE")
	if err != nil {
		return src.DataFrame{}, fmt.Errorf("error finding PRICE column: %w", err)
	}

	carryContractIndex, err := findColumnIndex(header, "CARRY_CONTRACT")
	if err != nil {
		return src.DataFrame{}, fmt.Errorf("error finding CARRY_CONTRACT column: %w", err)
	}

	forwardContractIndex, err := findColumnIndex(header, "FORWARD_CONTRACT")
	if err != nil {
		return src.DataFrame{}, fmt.Errorf("error finding FORWARD_CONTRACT column: %w", err)
	}

	priceContractIndex, err := findColumnIndex(header, "PRICE_CONTRACT")
	if err != nil {
		return src.DataFrame{}, fmt.Errorf("error finding PRICE_CONTRACT column: %w", err)
	}

	// Step 3: Process all rows
	processedRecords, err := processMultiplePricesRows(reader, priceIndex, carryContractIndex, forwardContractIndex, priceContractIndex, symbol)
	if err != nil {
		return src.DataFrame{}, fmt.Errorf("error processing rows: %w", err)
	}

	return src.DataFrame{
		SymbolName: symbol.Values[0],
		Records:    processedRecords,
	}, nil
}

// processMultiplePricesRows processes each row, parses and rounds the price, and appends the symbol.
func processMultiplePricesRows(reader *csv.Reader, priceIndex int, carryContractIndex int, forwardContractIndex int, priceContractIndex int, symbol src.CSVRecord) ([]src.CSVRecord, error) {
	var processedRecords []src.CSVRecord

	for {
		row, err := reader.Read()
		if err != nil {
			if err.Error() == "EOF" {
				break // End of file reached
			}
			return nil, fmt.Errorf("failed to read row: %w", err)
		}

		// Skip rows where the price field is empty
		if row[priceIndex] == "" {
			continue // Silently skip rows with an empty price field
		}

		// Parse and round the price
		price, err := parseAndRoundFloat(row, priceIndex, 3)
		if err != nil {
			return nil, fmt.Errorf("error parsing price: %w", err)
		}
		row[priceIndex] = price

		// Parse carry_contract as an integer
		carryContract, err := parseAndFormatInt(row, carryContractIndex)
		if err != nil {
			return nil, fmt.Errorf("error parsing carry_contract: %w", err)
		}
		row[carryContractIndex] = carryContract

		// Parse forward_contract as an integer
		forwardContract, err := parseAndFormatInt(row, forwardContractIndex)
		if err != nil {
			return nil, fmt.Errorf("error parsing forward_contract: %w", err)
		}
		row[forwardContractIndex] = forwardContract

		// Parse price_contract as an integer
		priceContract, err := parseAndFormatInt(row, priceContractIndex)
		if err != nil {
			return nil, fmt.Errorf("error parsing price_contract: %w", err)
		}
		row[priceContractIndex] = priceContract

		// Append the symbol to the row
		newRow := src.CSVRecord{
			Values: append(row, symbol.Values[0]),
		}
		processedRecords = append(processedRecords, newRow)
	}

	return processedRecords, nil
}
