package config_data_processing

import (
	"fmt"
	"main/src/models"
	"main/src/utils"
)

func finalizeMetadata(records []models.CSVRecord) ([]models.CSVRecord, error) {
	// Drop unnecessary columns
	columnsToDrop := []string{"SubSubClass", "Style", "Duration", "Description"}
	droppedRecords, err := utils.DropColumns(records, columnsToDrop)
	if err != nil {
		return nil, err
	}

	// Finalize the data
	finalRecords, err := FinishData(droppedRecords)
	if err != nil {
		return nil, err
	}

	return finalRecords, nil
}

// Function to process and update the 'sub_class' field based on 'symbol'
func FinishData(records []models.CSVRecord) ([]models.CSVRecord, error) {
	if len(records) == 0 {
		return nil, fmt.Errorf("no records found to process")
	}

	// Get column indexes for 'sub_class' and 'symbol'
	subClassIdx, err := utils.FindColumnIndex(records[0], "SubClass")
	if err != nil {
		return nil, err
	}

	symbolIdx, err := utils.FindColumnIndex(records[0], "Instrument")
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
