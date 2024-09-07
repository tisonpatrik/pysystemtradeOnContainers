package config_data_processing

import (
	"fmt"
	"log"
	"path/filepath"
	"starter/src"
	"starter/src/utils"
)

func CSVConfigProcessor(input src.ProcessorInput) error {
	// Use the struct fields instead of separate arguments
	fullPath := filepath.Join(input.Path, input.Name)
	filename := filepath.Base(fullPath)

	// Check the file name and call the appropriate function
	if filename == "moreinstrumentinfo.csv" {
		generate_metadata(fullPath, input.Symbols, input.NewColumnsNames)
	} else {
		generate_config_file(fullPath, input.Symbols, input.NewColumnsNames)
	}

	return nil
}

func generate_metadata(filePath string, symbols []src.CSVRecord, columns []string) {
	fmt.Printf("Generating metadata for file: %s\n", filePath)

	// Read the CSV file
	records, err := utils.ReadCSVFile(filePath)
	if err != nil {
		log.Fatalf("Failed to read the CSV file: %v", err)
	}

	// Rename columns using the new function
	records, err = utils.RenameCSVColumns(records, columns)
	if err != nil {
		log.Fatalf("Failed to rename columns: %v", err)
	}

	// Filter records based on symbols
	filteredRecords, err := utils.FilterRecordsBySymbols(records, "symbol", symbols)
	if err != nil {
		log.Fatalf("Failed to filter records: %v", err)
	}

	// Drop unnecessary columns
	columnsToDrop := []string{"sub_sub_class", "style", "country", "duration"}
	droppedRecords, err := utils.DropColumns(filteredRecords, columnsToDrop)
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
	if err := utils.SaveRecordsToCSV(outputDirectory, outputFilename, finalRecords); err != nil {
		log.Fatalf("Failed to save final records to CSV: %v", err)
	}

	fmt.Println("Metadata generation complete. Final records saved to CSV.")
}

func generate_config_file(filePath string, symbols []src.CSVRecord, columns []string) {
	fmt.Printf("Generating config file for: %s\n", filePath)
	// Read the CSV file
	records, err := utils.ReadCSVFile(filePath)
	if err != nil {
		log.Fatalf("Failed to read the CSV file: %v", err)
	}

	// Rename columns using the new function
	records, err = utils.RenameCSVColumns(records, columns)
	if err != nil {
		log.Fatalf("Failed to rename columns: %v", err)
	}

	// Filter records based on symbols
	filteredRecords, err := utils.FilterRecordsBySymbols(records, "symbol", symbols)
	if err != nil {
		log.Fatalf("Failed to filter records: %v", err)
	}
	// Save the final records to a CSV file
	outputDirectory := "data/csvconfig"
	outputFilename := filepath.Base(filePath)
	if err := utils.SaveRecordsToCSV(outputDirectory, outputFilename, filteredRecords); err != nil {
		log.Fatalf("Failed to save final records to CSV: %v", err)
	}

	fmt.Println("Metadata generation complete. Final records saved to CSV.")
}
