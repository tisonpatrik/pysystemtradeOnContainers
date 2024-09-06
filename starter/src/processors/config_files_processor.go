package processors

import (
	"fmt"
	"log"
	"path/filepath"
	"starter/src"
)

func CSVConfigProcessor(path string, name string, symbols [][]string, columns []string) error {
	fullPath := filepath.Join(path, name)
	filename := filepath.Base(fullPath)
	if filename == "moreinstrumentinfo.csv" {
		generate_metadata(fullPath, symbols, columns)
	} else {
		generate_config_file(fullPath, symbols, columns)
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

	// Drop unnecessary columns
	columnsToDrop := []string{"sub_sub_class", "style", "country", "duration"}
	droppedRecords, err := DropColumns(filteredRecords, columnsToDrop)
	if err != nil {
		log.Fatalf("Failed to drop columns: %v", err)
	}

	// Process the dropped records to finalize the data
	finalRecords, err := FinishData(droppedRecords)
	if err != nil {
		log.Fatalf("Failed to finalize data: %v", err)
	}

	// Save the final records to a CSV file
	outputDirectory := "data/csvconfig"
	outputFilename := filepath.Base(filePath)
	if err := src.SaveRecordsToCSV(outputDirectory, outputFilename, finalRecords); err != nil {
		log.Fatalf("Failed to save final records to CSV: %v", err)
	}

	fmt.Println("Metadata generation complete. Final records saved to CSV.")
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
	// Save the final records to a CSV file
	outputDirectory := "data/csvconfig"
	outputFilename := filepath.Base(filePath)
	if err := src.SaveRecordsToCSV(outputDirectory, outputFilename, filteredRecords); err != nil {
		log.Fatalf("Failed to save final records to CSV: %v", err)
	}

	fmt.Println("Metadata generation complete. Final records saved to CSV.")
}
