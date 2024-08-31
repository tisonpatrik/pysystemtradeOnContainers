package processors

import (
	"fmt"
	"path/filepath"
	"starter/src"
)

func ProcessData(dirPath string) error {
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

	// Placeholder for processing the downloaded subdmirectories
	for _, dir := range directories {
		// Get the base name of the directory
		baseName := filepath.Base(dir)
		fmt.Printf("Processing directory: %s\n", baseName)
		// Use a switch to handle different cases based on the directory name
		switch baseName {
		case "csvconfig":
			err := CSVConfigProcessor(dir, symbols)
			if err != nil {
				return fmt.Errorf("error processing csvconfig: %v", err)
			}
		case "adjusted_prices_csv":
			err := AdjustedPricesProcessor(dir, symbols)
			if err != nil {
				return fmt.Errorf("error processing adjusted prices: %v", err)
			}
		case "multiple_prices_csv":
			err := MultiplePricesProcessor(dir, symbols)
			if err != nil {
				return fmt.Errorf("error processing multiple prices: %v", err)
			}
		case "fx_prices_csv":
			err := FXPricesProcessor(dir, symbols)
			if err != nil {
				return fmt.Errorf("error processing fx prices: %v", err)
			}
		case "roll_calendars_csv":
			err := RollCalendarsProcessor(dir, symbols)
			if err != nil {
				return fmt.Errorf("error processing roll calendars: %v", err)
			}
		default:
			fmt.Printf("No specific processor for directory: %s\n", baseName)
		}
	}
	return nil
}
