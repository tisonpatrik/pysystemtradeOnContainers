package config_data_processing

import (
	"fmt"
	"log"
	"path/filepath"
	"starter/src"
	"starter/src/utils"
)

func CSVConfigProcessor(input src.ProcessorInput) error {
	fullPath := filepath.Join(input.Path, input.Name)
	filename := filepath.Base(fullPath)

	// Check the file name and process accordingly
	if filename == "moreinstrumentinfo.csv" {
		processFile(fullPath, input.Symbols, input.NewColumnsNames, true)
	} else {
		processFile(fullPath, input.Symbols, input.NewColumnsNames, false)
	}

	return nil
}

func processFile(filePath string, symbols []src.CSVRecord, columns []string, isMetadata bool) {
	// Read the CSV file
	records, err := utils.ReadCSVFile(filePath)
	if err != nil {
		log.Fatalf("Failed to read the CSV file: %v", err)
	}

	// Rename columns
	records, err = utils.RenameCSVColumns(records, columns)
	if err != nil {
		log.Fatalf("Failed to rename columns: %v", err)
	}

	// Filter records based on symbols
	filteredRecords, err := utils.FilterRecordsBySymbols(records, "symbol", symbols)
	if err != nil {
		log.Fatalf("Failed to filter records: %v", err)
	}

	// If generating metadata, drop unnecessary columns and finalize data
	var finalRecords []src.CSVRecord
	if isMetadata {
		finalRecords, err = finalizeMetadata(filteredRecords)
		if err != nil {
			log.Fatalf("Failed to finalize metadata: %v", err)
		}
	} else {
		finalRecords = filteredRecords
	}

	// Save the final records to a CSV file
	outputDirectory := "data/csvconfig"
	outputFilename := filepath.Base(filePath)
	if err := utils.SaveRecordsToCSV(outputDirectory, outputFilename, finalRecords); err != nil {
		log.Fatalf("Failed to save final records to CSV: %v", err)
	}

	fmt.Println(outputFilename + " generation complete. Final records saved to CSV.")
}

func finalizeMetadata(records []src.CSVRecord) ([]src.CSVRecord, error) {
	// Drop unnecessary columns
	columnsToDrop := []string{"sub_sub_class", "style", "country", "duration"}
	droppedRecords, err := utils.DropColumns(records, columnsToDrop)
	if err != nil {
		return nil, err
	}

	// Finalize the data
	finalRecords, err := FinishData(droppedRecords)
	if err != nil {
		return nil, err
	}

	return finalRecords, nil
}
