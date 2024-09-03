package processors

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"starter/src"
)

// Define a type for processor functions
type ProcessorFunc func(string, [][]string, []string) error

// ProcessData processes the data in the downloaded directories based on the mappings.
func ProcessData(dirPath string) error {
	// Load mappings from JSON
	mappingsPath := "starter/mappings.json"
	mappings, err := loadMappings(mappingsPath)
	if err != nil {
		return fmt.Errorf("error loading mappings: %w", err)
	}

	// Call DownloadData to download required data
	err = DownloadData(dirPath)
	if err != nil {
		return err
	}

	tradableInstrumentsCSV := "starter/tradable_instruments.csv"
	symbols, err := src.ReadCSVFile(tradableInstrumentsCSV)
	if err != nil {
		return err
	}

	// Define the map of processors based on directory name (Path)
	processors := map[string]ProcessorFunc{
		"csvconfig":           CSVConfigProcessor,
		"adjusted_prices_csv": AdjustedPricesProcessor,
		"multiple_prices_csv": MultiplePricesProcessor,
		"fx_prices_csv":       FXPricesProcessor,
		"roll_calendar_csv":   RollCalendarsProcessor,
	}

	// Process each mapping entry
	for _, record := range mappings {
		fmt.Printf("Processing file: %s in directory: %s\n", record.Name, record.Path)

		// Construct the full path to the file
		fullPath := filepath.Join(record.Path, record.Name)
		// Get the base directory name and find the appropriate processor
		baseDir := filepath.Base(record.Path)
		processor, exists := processors[baseDir]
		if !exists {
			fmt.Printf("No specific processor for directory: %s\n", baseDir)
			continue
		}

		// Call the processor function
		err := processor(fullPath, symbols, record.Columns)
		if err != nil {
			return fmt.Errorf("error processing %s: %v", baseDir, err)
		}
	}

	return nil
}

// loadMappings loads the JSON mappings file.
func loadMappings(filePath string) (Collection, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, fmt.Errorf("error opening mappings JSON file: %w", err)
	}
	defer file.Close()

	var records Collection
	if err := json.NewDecoder(file).Decode(&records); err != nil {
		return nil, fmt.Errorf("error decoding mappings JSON: %w", err)
	}

	return records, nil
}
