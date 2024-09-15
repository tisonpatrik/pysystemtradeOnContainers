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

// CSVConfigProcessor processes a single CSV file, filters rows based on the provided symbols, and writes the result to a new file.
func CSVConfigProcessor(input models.ProcessorInput) error {
	// Ensure the output directory exists
	outputDir := filepath.Join("database/data", "config_data")
	if err := os.MkdirAll(outputDir, os.ModePerm); err != nil {
		return fmt.Errorf("failed to create directory: %w", err)
	}

	// Open the CSV file
	file, err := utils.OpenCSVFile(input.Path, strings.TrimSuffix(input.Name, ".csv"))
	if err != nil {
		return fmt.Errorf("error opening CSV file %s: %w", input.Name, err)
	}
	defer file.Close()

	reader := csv.NewReader(file)

	// Filter rows based on symbols
	filteredRecords, err := filterRecords(reader, input.Symbols, input.Name)
	if err != nil {
		return fmt.Errorf("error filtering records: %w", err)
	}

	// Write the filtered data to a new CSV file
	outputPath := filepath.Join(outputDir, input.Name)
	if err := utils.WriteCSVFile(outputPath, input.NewColumnsNames, filteredRecords); err != nil {
		return fmt.Errorf("error writing filtered CSV: %w", err)
	}

	fmt.Println(input.Name + " generation complete. Filtered records saved to CSV.")
	return nil
}

// getHeader reads the CSV header and returns a map of column names to their indices and the header slice.
func getHeader(reader *csv.Reader) (map[string]int, []string, error) {
	header, err := reader.Read()
	if err != nil {
		return nil, nil, fmt.Errorf("failed to read header: %w", err)
	}

	columnIndices := make(map[string]int)
	for idx, colName := range header {
		columnIndices[colName] = idx
	}

	return columnIndices, header, nil
}

// filterRecords filters rows from the CSV based on the provided symbols and modifies columns if necessary.
func filterRecords(reader *csv.Reader, symbols models.Symbols, inputName string) ([]models.CSVRecord, error) {

	// Get the header and column indices
	headerMap, header, err := getHeader(reader)
	if err != nil {
		return nil, err
	}

	symbolIndex, exists := headerMap["Instrument"]
	if !exists {
		return nil, fmt.Errorf("'Instrument' column not found in CSV")
	}

	var removeIndices []int
	var subClassIndex int
	if inputName == "moreinstrumentinfo.csv" {
		subClassIndex, removeIndices, err = prepareSpecialCaseColumns(headerMap)
		if err != nil {
			return nil, err
		}
		header = removeColumns(header, removeIndices)
	}

	return processRows(reader, symbols, symbolIndex, subClassIndex, removeIndices, inputName == "moreinstrumentinfo.csv")
}

// prepareSpecialCaseColumns finds the indices of columns that need to be modified or removed for "moreinstrumentinfo.csv".
func prepareSpecialCaseColumns(headerMap map[string]int) (int, []int, error) {
	subClassIndex, exists := headerMap["SubClass"]
	if !exists {
		return 0, nil, fmt.Errorf("'SubClass' column not found in 'moreinstrumentinfo.csv'")
	}

	removeColumns := []string{"SubSubClass", "Style", "Country", "Duration", "Description"}
	removeIndices := findColumnIndices(headerMap, removeColumns)

	return subClassIndex, removeIndices, nil
}

// findColumnIndices returns the indices of the specified columns that exist in the header.
func findColumnIndices(headerMap map[string]int, columns []string) []int {
	var indices []int
	for _, col := range columns {
		if idx, exists := headerMap[col]; exists {
			indices = append(indices, idx)
		}
	}
	return indices
}

// processRows processes each row, filtering by symbol and applying modifications if necessary.
func processRows(reader *csv.Reader, symbolSet map[string]struct{}, symbolIndex, subClassIndex int, removeIndices []int, isSpecialCase bool) ([]models.CSVRecord, error) {
	var filteredRecords []models.CSVRecord

	for {
		row, err := reader.Read()
		if err != nil {
			if err.Error() == "EOF" {
				break
			}
			return nil, fmt.Errorf("failed to read row: %w", err)
		}

		if _, exists := symbolSet[row[symbolIndex]]; exists {
			if isSpecialCase {
				modifySubClass(row, symbolIndex, subClassIndex)
				row = removeColumns(row, removeIndices)
			}
			filteredRecords = append(filteredRecords, models.CSVRecord{Values: row})
		}
	}

	return filteredRecords, nil
}

// modifySubClass updates the SubClass column based on the Instrument value.
func modifySubClass(row []string, symbolIndex, subClassIndex int) {
	switch row[symbolIndex] {
	case "V2X":
		row[subClassIndex] = "EU-Vol"
	case "VIX":
		row[subClassIndex] = "VIX_mini"
	case "VNKI":
		row[subClassIndex] = "JPY-Vol"
	}
}

// removeColumns removes columns from a row by their indices.
func removeColumns(row []string, indices []int) []string {
	for i := len(indices) - 1; i >= 0; i-- {
		row = append(row[:indices[i]], row[indices[i]+1:]...)
	}
	return row
}
