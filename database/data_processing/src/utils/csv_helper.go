package utils

import (
	"encoding/csv"
	"fmt"
	"main/src/models"
)

func FindColumnIndex(record models.CSVRecord, columnName string) (int, error) {
	if len(record.Columns) == 0 {
		return -1, fmt.Errorf("no columns found in the CSV record")
	}

	for i, colName := range record.Columns {
		if colName == columnName {
			return i, nil
		}
	}
	return -1, fmt.Errorf("column %s not found in the record", columnName)
}

func RenameCSVColumns(records []models.CSVRecord, newColumnNames []string) ([]models.CSVRecord, error) {
	// Ensure there are records
	if len(records) == 0 {
		return nil, fmt.Errorf("no records found")
	}

	// Ensure the number of columns matches the number of newColumnNames
	if len(records[0].Columns) != len(newColumnNames) {
		return nil, fmt.Errorf("mismatch between the number of columns in the CSV and the provided new column names")
	}

	// Update the column names for all records
	for i := range records {
		records[i].Columns = newColumnNames
	}

	return records, nil
}

// GetHeader reads the CSV header and returns a map of column names to their indices and the header slice.
func GetHeader(reader *csv.Reader) (map[string]int, []string, error) {
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
