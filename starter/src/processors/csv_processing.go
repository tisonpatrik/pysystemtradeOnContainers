package processors

import (
	"fmt"
	"time"
)

// FindColumnIndex is a helper method that returns the index of a given column name in the records.
// It returns an error if the column is not found.
func FindColumnIndex(records [][]string, columnName string) (int, error) {
	if len(records) == 0 {
		return -1, fmt.Errorf("no records found in the CSV file")
	}

	for i, colName := range records[0] {
		if colName == columnName {
			return i, nil
		}
	}
	return -1, fmt.Errorf("column %s not found in the records", columnName)
}

// RenameCSVColumns renames the columns of the CSV records to the provided new column names.
// It returns an error if the number of new column names does not match the existing columns.
func RenameCSVColumns(records [][]string, newColumnNames []string) ([][]string, error) {
	if len(records) == 0 {
		return nil, fmt.Errorf("no records found in the CSV file")
	}

	if len(records[0]) != len(newColumnNames) {
		return nil, fmt.Errorf("mismatch between the number of columns in the CSV and the provided column names")
	}

	// Rename the columns
	for i := range records[0] {
		records[0][i] = newColumnNames[i]
	}

	return records, nil
}

// FilterRecordsBySymbols filters the CSV records based on a specified column and a list of symbols.
// It returns a new set of records that include only the rows where the specified column's value is in the symbols list.
func FilterRecordsBySymbols(records [][]string, columnName string, symbols []string) ([][]string, error) {
	if len(records) == 0 {
		return nil, fmt.Errorf("no records found in the CSV file")
	}

	// Use the helper method to find the column index
	colIndex, err := FindColumnIndex(records, columnName)
	if err != nil {
		return nil, err
	}

	// Create a map for quick lookup of symbols
	symbolSet := make(map[string]struct{})
	for _, symbol := range symbols {
		symbolSet[symbol] = struct{}{}
	}

	// Filter the records
	var filteredRecords [][]string
	filteredRecords = append(filteredRecords, records[0]) // include header

	for rowIndex, record := range records[1:] {
		if colIndex >= len(record) {
			return nil, fmt.Errorf("record %d has fewer columns than expected", rowIndex+2) // +2 to account for header and zero indexing
		}
		if _, exists := symbolSet[record[colIndex]]; exists {
			filteredRecords = append(filteredRecords, record)
		}
	}

	return filteredRecords, nil
}

// DropColumns removes specified columns from the CSV records.
// It returns a new set of records without the dropped columns.
func DropColumns(records [][]string, columnsToDrop []string) ([][]string, error) {
	if len(records) == 0 {
		return nil, fmt.Errorf("no records found in the CSV file")
	}

	// Find the indices of the columns to drop
	var dropIndices []int
	header := records[0]
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

	// Create a new records slice without the dropped columns
	var newRecords [][]string
	for _, record := range records {
		var newRecord []string
		for i, value := range record {
			// Only add columns that are not in dropIndices
			shouldDrop := false
			for _, dropIdx := range dropIndices {
				if i == dropIdx {
					shouldDrop = true
					break
				}
			}
			if !shouldDrop {
				newRecord = append(newRecord, value)
			}
		}
		newRecords = append(newRecords, newRecord)
	}

	return newRecords, nil
}

// ConvertDateToTime converts the specified time column in the CSV records to a standardized time format ("2006-01-02 15:04:05").
// It replaces invalid or unparsable dates with an empty string, similar to pandas' `errors="coerce"`.
// The function returns the updated records.
func ConvertDateToTime(records [][]string, timeColumnName string) ([][]string, error) {
	if len(records) == 0 {
		return nil, fmt.Errorf("no records found in the CSV file")
	}

	// Use the helper method to find the time column index
	timeColIndex, err := FindColumnIndex(records, timeColumnName)
	if err != nil {
		return nil, err
	}

	// Iterate over the records and convert the time column
	for i, record := range records[1:] { // Skip header
		if timeColIndex >= len(record) {
			return nil, fmt.Errorf("record %d has fewer columns than expected", i+2) // +2 for header and zero indexing
		}

		// Try parsing the time in RFC3339 format first
		parsedTime, err := time.Parse(time.RFC3339, record[timeColIndex])
		if err != nil {
			// If RFC3339 fails, try parsing in the specific "2006-01-02 15:04:05" format
			parsedTime, err = time.Parse("2006-01-02 15:04:05", record[timeColIndex])
			if err != nil {
				// If parsing fails, assign an empty string (similar to pandas `errors="coerce"`)
				records[i+1][timeColIndex] = ""
				continue
			}
		}

		// Format the parsed time as "2006-01-02 15:04:05" and overwrite the value in the record
		records[i+1][timeColIndex] = parsedTime.Format("2006-01-02 15:04:05")
	}

	return records, nil
}

func FillSymbolName(records [][]string, symbolName string) ([][]string, error) {
	// Check if "symbol" column exists, if not, add it as the first column.
	symbolColIdx, err := FindColumnIndex(records, "symbol")
	if err != nil {
		// If "symbol" column doesn't exist, we need to add it
		// Create a new header with the "symbol" column
		newRecords := [][]string{{"symbol"}}
		newRecords[0] = append(newRecords[0], records[0]...) // Add existing headers

		// Add symbol name to each row and append to the new records
		for _, record := range records[1:] {
			newRecord := append([]string{symbolName}, record...)
			newRecords = append(newRecords, newRecord)
		}
		return newRecords, nil
	}

	// If "symbol" column exists, fill it with the symbol name
	for i := 1; i < len(records); i++ { // Skip header
		records[i][symbolColIdx] = symbolName
	}
	return records, nil
}
func ConcatenateDataFrames(dataFrames [][][]string) ([][]string, error) {
	if len(dataFrames) == 0 {
		return nil, fmt.Errorf("no data frames to concatenate")
	}

	// Use the header of the first data frame
	concatenated := dataFrames[0]

	// Append rows from subsequent data frames
	for _, df := range dataFrames[1:] {
		concatenated = append(concatenated, df[1:]...) // Skip header row for subsequent data frames
	}

	return concatenated, nil
}
