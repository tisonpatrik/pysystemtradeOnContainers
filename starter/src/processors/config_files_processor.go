package processors

import (
	"fmt"
	"log"
	"path/filepath"
	"starter/src"
	"strings"
)

func CSVConfigProcessor(dir string, symbols [][]string, columns []string) error {
	// Inform about the processing directory
	fmt.Printf("Processing CSV config in directory: %s\n", dir)

	// Get all CSV files in the directory
	csvFiles, err := src.GetCSVFiles(dir)
	if err != nil {
		log.Fatalf("Failed to get CSV files: %v", err)
	}
	// Check for specific file and call appropriate methods
	for _, file := range csvFiles {
		if strings.EqualFold(file, "moreinstrumentinfo.csv") {
			fmt.Println("Found moreinstrumentinfo.csv, generating metadata...")
			generate_metadata(filepath.Join(dir, file))
		} else {
			fmt.Printf("Processing %s with generate_config_file...\n", file)
			generate_config_file(filepath.Join(dir, file))
		}
	}

	return nil
}

func generate_metadata(filePath string) {
	fmt.Printf("Generating metadata for file: %s\n", filePath)
	// Implement metadata generation logic here
}

func generate_config_file(filePath string) {
	fmt.Printf("Generating config file for: %s\n", filePath)
	// Implement config file generation logic here
}
