package processors

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"starter/src"
)

// ProcessData processes the data in the downloaded directories based on the mappings.
func ProcessData(dirPath string) error {
	// Load mappings from JSON
	mappingsPath := "starter/mappings.json"
	mappings, err := loadMappings(mappingsPath)
	if err != nil {
		return fmt.Errorf("error loading mappings: %w", err)
	}

	// Call DownloadData and get the list of successfully downloaded directories
	directories, err := DownloadData(dirPath)
	if err != nil {
		return err
	}

	tradableInstrumentsCSV := "starter/tradable_instruments.csv"
	symbols, err := src.ReadCSVFile(tradableInstrumentsCSV)
	if err != nil {
		return err
	}

	// Process each downloaded directory
	for _, dir := range directories {
		// Get the base name of the directory
		baseName := filepath.Base(dir)
		fmt.Printf("Processing directory: %s\n", baseName)

		// Find the matching mapping record
		for _, record := range mappings {
			if filepath.Base(record.Path) == baseName {
				switch baseName {
				case "csvconfig":
					err := CSVConfigProcessor(dir, symbols, record.Columns)
					if err != nil {
						return fmt.Errorf("error processing csvconfig: %v", err)
					}
				case "adjusted_prices_csv":
					err := AdjustedPricesProcessor(dir, symbols, record.Columns)
					if err != nil {
						return fmt.Errorf("error processing adjusted prices: %v", err)
					}
				case "multiple_prices_csv":
					err := MultiplePricesProcessor(dir, symbols, record.Columns)
					if err != nil {
						return fmt.Errorf("error processing multiple prices: %v", err)
					}
				case "fx_prices_csv":
					err := FXPricesProcessor(dir, symbols, record.Columns)
					if err != nil {
						return fmt.Errorf("error processing fx prices: %v", err)
					}
				case "roll_calendars_csv":
					err := RollCalendarsProcessor(dir, symbols, record.Columns)
					if err != nil {
						return fmt.Errorf("error processing roll calendars: %v", err)
					}
				default:
					fmt.Printf("No specific processor for directory: %s\n", baseName)
				}
				break
			}
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
