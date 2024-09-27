package raw_data_processing

import (
	"encoding/csv"
	"fmt"
	"main/src/models"
	"main/src/utils"
	"os"
	"path/filepath"
	"strconv"
)

// readHeaderAndFindColumn reads the CSV header and finds the index of the specified column.
func readHeaderAndFindColumn(reader *csv.Reader, columnName string) (int, error) {
	header, err := reader.Read()
	if err != nil {
		return -1, fmt.Errorf("failed to read header: %w", err)
	}

	index, err := findColumnIndex(header, columnName)
	if err != nil {
		return -1, fmt.Errorf("failed to find column %s in header %v: %w", columnName, header, err)
	}

	return index, nil
}

// findColumnIndex finds the index of a column with the given name in the header row.
func findColumnIndex(header []string, columnName string) (int, error) {
	for i, column := range header {
		if column == columnName {
			return i, nil
		}
	}
	return -1, fmt.Errorf("column %s not found in CSV", columnName)
}

// parseAndRoundFloat parses a value from a row based on the column index, converts it to a float, and rounds it to the specified decimal places.
func parseAndRoundFloat(row []string, colIndex int, decimalPlaces int) (string, error) {
	// Parse the value at the found index
	value := row[colIndex]
	floatValue, err := strconv.ParseFloat(value, 64)
	if err != nil {
		return "", fmt.Errorf("error parsing value at index %d: %w", colIndex, err)
	}

	// Round the float value to the specified decimal places
	format := fmt.Sprintf("%%.%df", decimalPlaces)
	roundedValue := fmt.Sprintf(format, floatValue)

	return roundedValue, nil
}

// parseAndFormatInt parses a value from a row based on the column index and converts it to an integer.
func parseAndFormatInt(row []string, colIndex int) (string, error) {
	// Parse the value at the specified index
	value := row[colIndex]
	intValue, err := strconv.Atoi(value)
	if err != nil {
		return "", fmt.Errorf("error parsing integer value at index %d: %w", colIndex, err)
	}

	// Return the integer value formatted as a string
	return strconv.Itoa(intValue), nil
}

// writeBatchToCSV writes a batch of CSV records to a file.
func writeBatchToCSV(outputPath string, columns []string, records []models.CSVRecord) error {
	// Ensure the directory exists
	dir := filepath.Dir(outputPath)
	err := os.MkdirAll(dir, os.ModePerm)
	if err != nil {
		return fmt.Errorf("error creating directory %s: %w", dir, err)
	}

	// Write the CSV file
	columns = append(columns, "symbol")
	err = utils.WriteCSVFile(outputPath, columns, records)
	if err != nil {
		return fmt.Errorf("error writing CSV file: %w", err)
	}
	return nil
}
