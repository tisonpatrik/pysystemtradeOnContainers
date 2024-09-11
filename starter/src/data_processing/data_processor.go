package data_processing

import (
	"fmt"
	"path/filepath"
	"starter/src"
	"starter/src/data_processing/config_data_processing"
	"starter/src/data_processing/raw_data_processing"
	"starter/src/utils"
	"sync"
	"time"
)

// ProcessData processes the data in the downloaded directories based on the mappings.
func ProcessData(dirPath string) error {
	startTime := time.Now()

	// Load mappings from JSON
	mappings, err := utils.LoadJSONfile("starter/mappings.json")
	if err != nil {
		return fmt.Errorf("error loading mappings: %w", err)
	}

	// Download required data
	if err := DownloadData(dirPath); err != nil {
		return err
	}

	// Load symbols from CSV
	symbols, err := utils.ReadCSVFile("starter/tradable_instruments.csv")
	if err != nil {
		return err
	}

	// Define and execute processors
	processors := defineProcessors()
	if err := processMappingsConcurrently(mappings, symbols, processors); err != nil {
		return err
	}

	elapsedTime := time.Since(startTime)
	fmt.Printf("The ProcessData function took: %s\n", elapsedTime)
	return nil
}

// defineProcessors returns a map of processor functions.
func defineProcessors() map[string]src.ProcessorFunc {
	return map[string]src.ProcessorFunc{
		"csvconfig":           config_data_processing.CSVConfigProcessor,
		"adjusted_prices_csv": raw_data_processing.AdjustedPricesProcessor,
		"multiple_prices_csv": raw_data_processing.MultiplePricesProcessor,
		"fx_prices_csv":       raw_data_processing.FXPricesProcessor,
		"roll_calendars_csv":  raw_data_processing.RollCalendarsProcessor,
	}
}

// processMappingsConcurrently processes each mapping concurrently using goroutines.
func processMappingsConcurrently(mappings []src.Mapping, symbols []src.CSVRecord, processors map[string]src.ProcessorFunc) error {
	var wg sync.WaitGroup
	errChan := make(chan error, len(mappings)) // Buffered error channel
	sem := make(chan struct{}, 10)             // Semaphore to limit the number of concurrent goroutines

	for _, record := range mappings {
		wg.Add(1)

		go func(record src.Mapping) {
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
func processMapping(record src.Mapping, symbols []src.CSVRecord, processors map[string]src.ProcessorFunc) error {
	fmt.Printf("Processing file: %s in directory: %s\n", record.Name, record.Path)

	baseDir := filepath.Base(record.Path)
	processor, exists := processors[baseDir]
	if !exists {
		fmt.Printf("No specific processor for directory: %s\n", baseDir)
		return nil
	}

	input := src.ProcessorInput{
		Path:            record.Path,
		Name:            record.Name,
		Symbols:         symbols,
		NewColumnsNames: record.Columns,
	}

	if err := processor(input); err != nil {
		return fmt.Errorf("error processing %s: %v", baseDir, err)
	}
	fmt.Println("")
	return nil
}
