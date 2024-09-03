package processors

import (
	"fmt"
)

// Function to determine the subclass based on the symbol
func determineSubClass(symbol, currentSubClass string) string {
	if currentSubClass != "" {
		return currentSubClass
	}

	switch symbol {
	case "V2X":
		return "EU-Vol"
	case "VIX", "VIX_mini":
		return "US-Vol"
	case "VNKI":
		return "JPY-Vol"
	default:
		return "" // or a default value if needed
	}
}

// Function to find the index of a column by name
func findColumnIndex(header []string, columnName string) (int, error) {
	for i, colName := range header {
		if colName == columnName {
			return i, nil
		}
	}
	return -1, fmt.Errorf("column %s not found", columnName)
}

// Function to process and update the 'sub_class' field based on 'symbol'
func FinishData(records [][]string) ([][]string, error) {
	if len(records) == 0 {
		return nil, fmt.Errorf("no records found to process")
	}

	// Get column indexes for 'sub_class' and 'symbol'
	subClassIdx, err := findColumnIndex(records[0], "sub_class")
	if err != nil {
		return nil, err
	}

	symbolIdx, err := findColumnIndex(records[0], "symbol")
	if err != nil {
		return nil, err
	}

	// Update 'sub_class' based on 'symbol'
	for i := 1; i < len(records); i++ { // skip header
		records[i][subClassIdx] = determineSubClass(records[i][symbolIdx], records[i][subClassIdx])
	}

	return records, nil
}
