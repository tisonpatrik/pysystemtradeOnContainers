package config_data_processing

import (
	"encoding/csv"
	"fmt"
	"main/src/models"
	"main/src/utils"
	"os"
	"path/filepath"
	"strings"
)

// CSVConfigProcessor processes a single CSV file and filters rows based on the provided symbols.
func CSVConfigProcessor(input models.ProcessorInput) error {

	// Ensure the output directory exists before writing the final filtered CSV
	outputDir := filepath.Join("database/data", "config_data")
	if err := os.MkdirAll(outputDir, os.ModePerm); err != nil {
		return fmt.Errorf("failed to create directory: %w", err)
	}

	// Step 1: Open the CSV file
	file, err := utils.OpenCSVFile(input.Path, strings.TrimSuffix(input.Name, ".csv"))
	if err != nil {
		return fmt.Errorf("error opening CSV file %s: %w", input.Name, err)
	}
	defer file.Close()

	reader := csv.NewReader(file)

	// Step 3: Filter rows by the provided symbols
	filteredRecords, err := filterRecordsBySymbols(reader, input.Symbols, input.Name)
	if err != nil {
		return fmt.Errorf("error filtering records: %w", err)
	}

	// Step 4: Write the filtered (and potentially updated) data to a new CSV file
	err = utils.WriteCSVFile(filepath.Join(outputDir, input.Name), input.NewColumnsNames, filteredRecords)
	if err != nil {
		return fmt.Errorf("error writing filtered CSV: %w", err)
	}

	fmt.Println(input.Name + " generation complete. Filtered records saved to CSV.")
	return nil
}

// getHeader reads the header from the CSV and returns a map of all column names and their indices.
func getHeader(reader *csv.Reader) (map[string]int, []string, error) {
	// Read the header
	header, err := reader.Read()
	if err != nil {
		return nil, nil, fmt.Errorf("failed to read header: %w", err)
	}

	// Create a map to store column indices
	columnIndices := make(map[string]int)

	// Populate the map with column names and their respective indices
	for index, colName := range header {
		columnIndices[colName] = index
	}

	return columnIndices, header, nil
}

// filterRecordsBySymbols filters rows from a CSV based on the provided symbols and column index.
func filterRecordsBySymbols(reader *csv.Reader, symbols []models.CSVRecord, inputName string) ([]models.CSVRecord, error) {
	var filteredRecords []models.CSVRecord
	symbolSet := make(map[string]struct{})

	// Populate symbol set for fast lookup
	for _, symbolRecord := range symbols {
		if len(symbolRecord.Values) > 0 {
			symbolSet[symbolRecord.Values[0]] = struct{}{}
		}
	}

	// Step 1: Get header from CSV
	headerMap, header, err := getHeader(reader)
	if err != nil {
		return nil, err
	}

	// Step 2: Get symbol index (Instrument column must exist)
	symbolIndex, ok := headerMap["Instrument"]
	if !ok {
		return nil, fmt.Errorf("'Instrument' column not found in CSV")
	}

	// Step 3: Optional: Get subclass index only for "moreinstrumentinfo.csv"
	var subClassIndex int
	var removeIndices []int

	if inputName == "moreinstrumentinfo.csv" {
		subClassIndex, ok = headerMap["SubClass"]
		if !ok {
			return nil, fmt.Errorf("'SubClass' column not found in 'moreinstrumentinfo.csv'")
		}

		// Identify the columns to remove by their indices
		removeColumns := []string{"SubSubClass", "Style", "Country", "Duration", "Description"}
		for _, col := range removeColumns {
			if idx, exists := headerMap[col]; exists {
				removeIndices = append(removeIndices, idx)
			}
		}

		// Remove the specified columns from the header as well
		header = removeColumnsByIndices(header, removeIndices)
	}

	// Step 4: Process and filter rows
	for {
		row, err := reader.Read()
		if err != nil {
			if err.Error() == "EOF" {
				break
			}
			return nil, fmt.Errorf("failed to read row: %w", err)
		}

		// Check if the row contains a symbol that needs to be filtered
		if _, exists := symbolSet[row[symbolIndex]]; exists {
			// If the input file is "moreinstrumentinfo.csv", modify the row
			if inputName == "moreinstrumentinfo.csv" {
				// Modify SubClass based on Instrument values
				switch row[symbolIndex] {
				case "V2X":
					row[subClassIndex] = "EU-Vol"
				case "VIX":
					row[subClassIndex] = "VIX_mini"
				case "VNKI":
					row[subClassIndex] = "JPY-Vol"
				}

				// Remove values for specified columns
				row = removeColumnsByIndices(row, removeIndices)
			}

			// Append the filtered (and potentially modified) record
			filteredRecords = append(filteredRecords, models.CSVRecord{Values: row})
		}
	}

	return filteredRecords, nil
}

// removeColumnsByIndices removes columns from a row by their indices.
func removeColumnsByIndices(row []string, indices []int) []string {
	// Sort indices in descending order to avoid index shifting issues during removal
	for i := len(indices) - 1; i >= 0; i-- {
		idx := indices[i]
		row = append(row[:idx], row[idx+1:]...)
	}
	return row
}
