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
