package processors

import "fmt"

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

func FilterRecordsBySymbols(records [][]string, columnName string, symbols []string) ([][]string, error) {
	if len(records) == 0 {
		return nil, fmt.Errorf("no records found in the CSV file")
	}

	// Find the index of the column that matches columnName
	colIndex := -1
	for i, colName := range records[0] {
		if colName == columnName {
			colIndex = i
			break
		}
	}

	if colIndex == -1 {
		return nil, fmt.Errorf("column %s not found in the records", columnName)
	}

	// Create a map for quick lookup of symbols
	symbolSet := make(map[string]struct{})
	for _, symbol := range symbols {
		symbolSet[symbol] = struct{}{}
	}

	// Filter the records
	var filteredRecords [][]string
	filteredRecords = append(filteredRecords, records[0]) // include header

	for _, record := range records[1:] {
		if _, exists := symbolSet[record[colIndex]]; exists {
			filteredRecords = append(filteredRecords, record)
		}
	}

	return filteredRecords, nil
}
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

	// Create new records without the dropped columns
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
