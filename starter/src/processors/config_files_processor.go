package processors

import (
	"fmt"
	"log"
	"path/filepath"
	"starter/src"
)

func CSVConfigProcessor(full_path string, symbols [][]string, columns []string) error {
	filename := filepath.Base(full_path)
	if filename == "moreinstrumentinfo.csv" {
		generate_metadata(full_path, symbols, columns)
	} else {
		generate_config_file(full_path, symbols, columns)
	}
	return nil
}

func generate_metadata(filePath string, symbols [][]string, columns []string) {
	fmt.Printf("Generating metadata for file: %s\n", filePath)

	// Read the CSV file
	records, err := src.ReadCSVFile(filePath)
	if err != nil {
		log.Fatalf("Failed to read the CSV file: %v", err)
	}

	// Rename columns using the new function
	records, err = RenameCSVColumns(records, columns)
	if err != nil {
		log.Fatalf("Failed to rename columns: %v", err)
	}

	symbolList := src.ConvertToSymbolList(symbols)

	// Filter records based on symbols
	filteredRecords, err := FilterRecordsBySymbols(records, "symbol", symbolList)
	if err != nil {
		log.Fatalf("Failed to filter records: %v", err)
	}

	// Additional logic for processing the filtered records can be implemented here

	// Print the number of records left after filtering (excluding the header)
	fmt.Printf("Number of records after filtering: %d\n", len(filteredRecords)-1)

	// Example output to verify the first filtered record
	if len(filteredRecords) > 1 {
		fmt.Println("First filtered record:", filteredRecords[1])
	}
}
func generate_config_file(filePath string, symbols [][]string, columns []string) {
	fmt.Printf("Generating config file for: %s\n", filePath)
	// Read the CSV file
	records, err := src.ReadCSVFile(filePath)
	if err != nil {
		log.Fatalf("Failed to read the CSV file: %v", err)
	}

	// Rename columns using the new function
	records, err = RenameCSVColumns(records, columns)
	if err != nil {
		log.Fatalf("Failed to rename columns: %v", err)
	}
	symbolList := src.ConvertToSymbolList(symbols)

	// Filter records based on symbols
	filteredRecords, err := FilterRecordsBySymbols(records, "symbol", symbolList)
	if err != nil {
		log.Fatalf("Failed to filter records: %v", err)
	}

	// Additional logic for processing the filtered records can be implemented here

	// Print the number of records left after filtering (excluding the header)
	fmt.Printf("Number of records after filtering: %d\n", len(filteredRecords)-1)

	// Example output to verify the first filtered record
	if len(filteredRecords) > 1 {
		fmt.Println("First filtered record:", filteredRecords[1])
	}
}
