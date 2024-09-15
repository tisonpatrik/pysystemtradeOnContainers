package src

import (
	"fmt"
	"main/src/config_data_processing"
	"main/src/data_downloader"
	"main/src/models"
	"main/src/raw_data_processing"
	"main/src/utils"
	"path/filepath"
	"sync"
)

// ProcessData processes the data in the downloaded directories based on the mappings.
func ProcessData(dirPath string) error {

	// Load mappings from JSON
	mappings, err := utils.LoadJSONfile("database/data_processing/configs/mappings.json")
	if err != nil {
		return fmt.Errorf("error loading mappings: %w", err)
	}

	// Download required data
	if err := data_downloader.DownloadData(dirPath); err != nil {
		return err
	}

	// Load symbols from CSV
	symbols, err := utils.ReadSymbolsFromCSV("database/data_processing/configs/tradable_instruments.csv")
	if err != nil {
		return err
	}

	// Define and execute processors
	processors := defineProcessors()
	if err := processMappingsConcurrently(mappings, symbols, processors); err != nil {
		return err
	}
	return nil
}

// defineProcessors returns a map of processor functions.
func defineProcessors() map[string]models.ProcessorFunc {
	return map[string]models.ProcessorFunc{
		"csvconfig":           config_data_processing.CSVConfigProcessor,
		"adjusted_prices_csv": raw_data_processing.AdjustedPricesProcessor,
		"multiple_prices_csv": raw_data_processing.MultiplePricesProcessor,
		"fx_prices_csv":       raw_data_processing.FXPricesProcessor,
		"roll_calendars_csv":  raw_data_processing.RollCalendarsProcessor,
	}
}

// processMappingsConcurrently processes each mapping concurrently using goroutines.
func processMappingsConcurrently(mappings []models.Mapping, symbols models.Symbols, processors map[string]models.ProcessorFunc) error {
	var wg sync.WaitGroup
	errChan := make(chan error, len(mappings)) // Buffered error channel
	sem := make(chan struct{}, 10)             // Semaphore to limit the number of concurrent goroutines

	for _, record := range mappings {
		wg.Add(1)

		go func(record models.Mapping) {
			defer wg.Done()
			sem <- struct{}{}        // Acquire semaphore to limit concurrency
			defer func() { <-sem }() // Release semaphore

			if err := processMapping(record, symbols, processors); err != nil {
				errChan <- err
			}
		}(record)
	}

	wg.Wait()
	close(errChan)

	// Collect all errors
	var errs []error
	for err := range errChan {
		if err != nil {
			errs = append(errs, err)
		}
	}

	if len(errs) > 0 {
		return fmt.Errorf("multiple errors occurred: %v", errs)
	}

	return nil
}

// processMapping processes an individual mapping.
func processMapping(record models.Mapping, symbols models.Symbols, processors map[string]models.ProcessorFunc) error {
	baseDir := filepath.Base(record.Path)
	processor, exists := processors[baseDir]
	if !exists {
		fmt.Printf("No specific processor for directory: %s\n", baseDir)
		return nil
	}

	input := models.ProcessorInput{
		Path:            record.Path,
		Name:            record.Name,
		Symbols:         symbols,
		NewColumnsNames: record.Columns,
	}

	if err := processor(input); err != nil {
		return fmt.Errorf("error processing %s: %v", baseDir, err)
	}
	return nil
}
