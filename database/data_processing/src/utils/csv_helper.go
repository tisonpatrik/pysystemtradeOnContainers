package utils

import (
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

func DropColumns(records []models.CSVRecord, columnsToDrop []string) ([]models.CSVRecord, error) {
	if len(records) == 0 {
		return nil, fmt.Errorf("no records found in the CSV file")
	}

	// Find the indices of the columns to drop
	var dropIndices []int
	header := records[0].Columns
	for i, colName := range header {
		for _, dropCol := range columnsToDrop {
			if colName == dropCol {
				dropIndices = append(dropIndices, i)
				break
			}
		}
	}

	// If no columns were found to drop, return the original records
	if len(dropIndices) == 0 {
		return records, nil
	}

	// Create new records without the dropped columns
	var newRecords []models.CSVRecord
	for _, record := range records {
		var newValues []string
		var newColumns []string

		// Remove the columns in the dropIndices
		for i, value := range record.Values {
			shouldDrop := false
			for _, dropIdx := range dropIndices {
				if i == dropIdx {
					shouldDrop = true
					break
				}
			}
			if !shouldDrop {
				newValues = append(newValues, value)
			}
		}

		// Remove the dropped columns from the Columns if it's not empty
		for i, col := range record.Columns {
			shouldDrop := false
			for _, dropIdx := range dropIndices {
				if i == dropIdx {
					shouldDrop = true
					break
				}
			}
			if !shouldDrop {
				newColumns = append(newColumns, col)
			}
		}

		// Create a new CSVRecord with the remaining columns and values
		newRecord := models.CSVRecord{
			Columns: newColumns,
			Values:  newValues,
		}
		newRecords = append(newRecords, newRecord)
	}

	return newRecords, nil
}
