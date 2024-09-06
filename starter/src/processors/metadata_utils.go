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

// Function to process and update the 'sub_class' field based on 'symbol'
func FinishData(records [][]string) ([][]string, error) {
	if len(records) == 0 {
		return nil, fmt.Errorf("no records found to process")
	}

	// Get column indexes for 'sub_class' and 'symbol'
	subClassIdx, err := FindColumnIndex(records, "sub_class")
	if err != nil {
		return nil, err
	}

	symbolIdx, err := FindColumnIndex(records, "symbol")
	if err != nil {
		return nil, err
	}

	// Update 'sub_class' based on 'symbol'
	for i := 1; i < len(records); i++ { // skip header
		records[i][subClassIdx] = determineSubClass(records[i][symbolIdx], records[i][subClassIdx])
	}

	return records, nil
}
