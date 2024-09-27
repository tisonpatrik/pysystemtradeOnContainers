package main

import (
	"bufio"
	"downloader/src"
	"fmt"
	"log"
	"os"
	"path/filepath"
	"strings"
)

func main() {
	fmt.Println("We are about to download and process data for the project.")

	// Get the project root directory (assuming this function is implemented)
	rootPath, err := src.GetProjectRoot()
	if err != nil {
		log.Fatalf("Error getting project root: %v", err)
		return
	}

	// Construct the path where the data should be downloaded
	dirPath := filepath.Join(rootPath, "data", "temp")

	// Check if the directory exists
	isExist, err := src.IsDirExists(dirPath)
	if err != nil {
		log.Fatalf("Error checking if directory exists: %v", err)
		return
	}

	// Check if the directory is empty (if it exists)
	var isEmpty bool
	if isExist {
		isEmpty, err = src.IsDirEmpty(dirPath)
		if err != nil {
			log.Fatalf("Error checking if directory is empty: %v", err)
			return
		}
	}

	// If directory exists and is not empty, prompt user for confirmation
	if isExist && !isEmpty {
		overwrite := askForConfirmation()
		if !overwrite {
			fmt.Println("Download aborted.")
			return
		} else {
			fmt.Println("Overwriting existing directory and downloading data...")
		}
	}

	// Call the DownloadData function from the src package
	err = src.DownloadData(dirPath)
	if err != nil {
		log.Fatalf("Error downloading data: %v", err)
		return
	}

	fmt.Println("Data download completed successfully!")
}

// askForConfirmation prompts the user with a yes/no question and returns true for "y" or false for "n".
func askForConfirmation() bool {
	reader := bufio.NewReader(os.Stdin)
	fmt.Print("Directory already exists and is not empty. Do you want to overwrite it? (y/N): ")
	input, _ := reader.ReadString('\n')
	input = strings.TrimSpace(strings.ToLower(input))
	return input == "y"
}
