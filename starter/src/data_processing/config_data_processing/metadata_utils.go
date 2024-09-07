package config_data_processing

import (
	"fmt"
	"starter/src"
	"starter/src/utils"
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
func FinishData(records []src.CSVRecord) ([]src.CSVRecord, error) {
	if len(records) == 0 {
		return nil, fmt.Errorf("no records found to process")
	}

	// Get column indexes for 'sub_class' and 'symbol'
	subClassIdx, err := utils.FindColumnIndex(records[0], "sub_class")
	if err != nil {
		return nil, err
	}

	symbolIdx, err := utils.FindColumnIndex(records[0], "symbol")
	if err != nil {
		return nil, err
	}

	// Update 'sub_class' based on 'symbol'
	for i := 1; i < len(records); i++ { // skip header
		// Access the Values field and update the 'sub_class' value
		records[i].Values[subClassIdx] = determineSubClass(records[i].Values[symbolIdx], records[i].Values[subClassIdx])
	}

	return records, nil
}
