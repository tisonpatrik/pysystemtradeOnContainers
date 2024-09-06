package processors

import (
	"fmt"
	"log"
	"path/filepath"
	"starter/src"
)

// AdjustedPricesProcessor processes adjusted prices based on CSV files in the directory and symbols.
func AdjustedPricesProcessor(path string, name string, symbols [][]string, columns []string) error {
	// Convert symbols into a list of strings
	listOfSymbols := src.ConvertToSymbolList(symbols)

	// Load the CSV files using LoadMultipleCSVFiles
	dataFramesDict, err := src.LoadMultipleCSVFiles(path, listOfSymbols, false)
	if err != nil {
		return fmt.Errorf("failed to load CSV files: %v", err)
	}

	var processedDataFrames [][][]string
	// Process each loaded CSV file
	for symbolName, records := range dataFramesDict {
		fmt.Printf("Processing symbol: %s with %d records\n", symbolName, len(records))

		// Rename the columns
		records, err = RenameCSVColumns(records, columns)
		if err != nil {
			log.Fatalf("Failed to rename columns: %v", err)
		}

		// Convert the "time" column to standardized format
		records, err = ConvertDateToTime(records, "time")
		if err != nil {
			log.Fatalf("Failed to convert date to time: %v", err)
		}

		// Fill the "symbol" column with the symbol name
		records, err = FillSymbolName(records, symbolName)
		if err != nil {
			log.Fatalf("Failed to fill symbol name: %v", err)
		}
		processedDataFrames = append(processedDataFrames, records)
	}

	// Concatenate all processed data frames into one
	concatenatedRecords, err := ConcatenateDataFrames(processedDataFrames)
	if err != nil {
		return fmt.Errorf("failed to concatenate data frames: %v", err)
	}

	// Save the final records to a CSV file
	outputDirectory := "data/adjusted_prices"
	outputFilename := filepath.Base(name)
	if err := src.SaveRecordsToCSV(outputDirectory, outputFilename, concatenatedRecords); err != nil {
		log.Fatalf("Failed to save final records to CSV: %v", err)
	}

	fmt.Println("Adjusted prices generation complete. Final records saved to CSV.")

	// Explicitly return nil to indicate success
	return nil
}
