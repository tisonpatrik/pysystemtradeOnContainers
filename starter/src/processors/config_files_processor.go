package processors

import (
	"fmt"
	"log"
	"starter/src"
)


func CSVConfigProcessor(dir string, symbols [][]string) error {
	// Inform about the processing directory
	fmt.Printf("Processing CSV config in directory: %s\n", dir)

	csvFiles, err := src.GetCSVFiles(dir)
	if err != nil {
		log.Fatalf("Failed to get CSV files: %v", err)
	}

	fmt.Println("CSV files found:", csvFiles)
	return nil
}
