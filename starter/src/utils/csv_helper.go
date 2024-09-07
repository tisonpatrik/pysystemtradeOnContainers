package utils

import (
	"fmt"
	"starter/src"
)

func FindColumnIndex(record src.CSVRecord, columnName string) (int, error) {
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

func RenameCSVColumns(records []src.CSVRecord, newColumnNames []string) ([]src.CSVRecord, error) {
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

// FilterRecordsBySymbols filters the records based on the provided symbols.
func FilterRecordsBySymbols(records []src.CSVRecord, columnName string, symbols []src.CSVRecord) ([]src.CSVRecord, error) {
	if len(records) == 0 {
		return nil, fmt.Errorf("no records found in the CSV file")
	}

	// Find the column index of the columnName in the header (Columns are the same for all records)
	colIndex, err := FindColumnIndex(records[0], columnName)
	if err != nil {
		return nil, err
	}

	// Extract symbol values from the symbols slice and store them in a map for quick lookup
	symbolSet := make(map[string]struct{})
	for _, symbolRecord := range symbols {
		if len(symbolRecord.Values) == 0 {
			continue // Skip if there are no values in the symbol record
		}
		// We assume the symbol is in the first value of the `Values` slice of the `CSVRecord`
		symbolSet[symbolRecord.Values[0]] = struct{}{}
	}

	// Filter the records
	var filteredRecords []src.CSVRecord

	// Iterate over all the records
	for _, record := range records {
		if colIndex >= len(record.Values) {
			return nil, fmt.Errorf("record has fewer columns than expected")
		}
		if _, exists := symbolSet[record.Values[colIndex]]; exists {
			filteredRecords = append(filteredRecords, record)
		}
	}

	return filteredRecords, nil
}

func DropColumns(records []src.CSVRecord, columnsToDrop []string) ([]src.CSVRecord, error) {
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
	var newRecords []src.CSVRecord
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
		newRecord := src.CSVRecord{
			Columns: newColumns,
			Values:  newValues,
		}
		newRecords = append(newRecords, newRecord)
	}

	return newRecords, nil
}

func FillSymbolName(records []src.CSVRecord, symbolName string) ([]src.CSVRecord, error) {
	if len(records) == 0 {
		return nil, fmt.Errorf("no records found")
	}

	// Iterate over each record and add the "symbol" column with the provided symbolName
	for i := range records {
		// Add "symbol" to the Columns if it's not present
		records[i].Columns = append(records[i].Columns, "symbol")

		// Add symbolName to the Values
		records[i].Values = append(records[i].Values, symbolName)
	}

	return records, nil
}

func ConcatenateDataFrames(dataFrames []src.DataFrame, symbolName string) (src.DataFrame, error) {
	var concatenatedRecords []src.CSVRecord

	for _, df := range dataFrames {
		concatenatedRecords = append(concatenatedRecords, df.Records...)
	}

	concatenatedDataFrame := src.DataFrame{
		SymbolName: symbolName,
		Records:    concatenatedRecords,
	}

	return concatenatedDataFrame, nil
}
