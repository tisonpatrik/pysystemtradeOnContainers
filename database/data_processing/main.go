package main

import (
	"fmt"
	"main/src"
	"main/src/utils"
)

func main() {
	fmt.Println("We are about to download and process data for project.")

	// Get the project root directory
	rootPath, err := utils.GetProjectRoot()
	if err != nil {
		fmt.Println("Error getting project root:", err)
		return
	}

	// Call the ProcessData function from the data_processing package
	if err := src.ProcessData(rootPath); err != nil {
		fmt.Println("Failed to download and process the data:", err)
		return
	}
}
