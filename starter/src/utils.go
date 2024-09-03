package src

import (
	"bufio"
	"encoding/csv"
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

// GetProjectRoot returns the project root path, assuming this file is in the init directory.
func GetProjectRoot() (string, error) {
	currentFilePath, err := os.Getwd() // Get current working directory
	if err != nil {
		return "", fmt.Errorf("error determining current working directory: %w", err)
	}

	// Return the parent directory of the current directory (which is assumed to be 'init')
	return filepath.Abs(filepath.Join(currentFilePath, ".."))
}

// CreateFile is a wrapper around os.Create to handle file creation.
func CreateFile(path string) (*os.File, error) {
	return os.Create(path)
}

// GetReader returns a bufio.Reader to read user input from stdin.
func GetReader() *bufio.Reader {
	return bufio.NewReader(os.Stdin)
}

// TrimSpace is a wrapper around strings.TrimSpace.
func TrimSpace(s string) string {
	return strings.TrimSpace(s)
}

// FileExists checks if a file exists at the given path.
func FileExists(path string) bool {
	_, err := os.Stat(path)
	return !os.IsNotExist(err)
}

// ReadEnvFile reads the .env file and returns its contents as a map of key-value pairs.
func ReadEnvFile(filePath string) (map[string]string, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	envVariables := make(map[string]string)
	scanner := bufio.NewScanner(file)

	for scanner.Scan() {
		line := TrimSpace(scanner.Text())
		if line == "" || strings.HasPrefix(line, "#") {
			continue // Skip empty lines and comments
		}

		parts := strings.SplitN(line, "=", 2)
		if len(parts) != 2 {
			return nil, fmt.Errorf("invalid line in .env file: %s", line)
		}

		key := TrimSpace(parts[0])
		value := TrimSpace(parts[1])
		envVariables[key] = value
	}

	if err := scanner.Err(); err != nil {
		return nil, err
	}

	return envVariables, nil
}

func ReadCSVFile(filePath string) ([][]string, error) {
	// Open the CSV file
	file, err := os.Open(filePath)
	if err != nil {
		return nil, fmt.Errorf("could not open the file: %v", err)
	}
	defer file.Close()

	// Create a new CSV reader
	reader := csv.NewReader(file)

	// Read all the records from the file
	records, err := reader.ReadAll()
	if err != nil {
		return nil, fmt.Errorf("could not read the CSV file: %v", err)
	}

	return records, nil
}

// GetCSVFiles returns a list of all CSV files in the specified directory.
func GetCSVFiles(dir string) ([]string, error) {
	var csvFiles []string

	// Read all files in the specified directory
	files, err := os.ReadDir(dir)
	if err != nil {
		return nil, fmt.Errorf("error reading directory: %w", err)
	}

	// Iterate over the files and add CSV files to the list
	for _, file := range files {
		if !file.IsDir() && filepath.Ext(file.Name()) == ".csv" {
			csvFiles = append(csvFiles, file.Name())
		}
	}

	return csvFiles, nil
}

func ConvertToSymbolList(symbols [][]string) []string {
	var symbolList []string
	for _, symbol := range symbols {
		if len(symbol) > 0 {
			symbolList = append(symbolList, symbol[0])
		}
	}
	return symbolList
}
func SaveRecordsToCSV(directory string, filename string, records [][]string) error {
	// Ensure the directory exists
	if err := os.MkdirAll(directory, os.ModePerm); err != nil {
		return fmt.Errorf("failed to create directory: %v", err)
	}

	// Create the CSV file
	filePath := filepath.Join(directory, filename)
	file, err := os.Create(filePath)
	if err != nil {
		return fmt.Errorf("failed to create file: %v", err)
	}
	defer file.Close()

	// Create a CSV writer and write the records to the file
	writer := csv.NewWriter(file)
	if err := writer.WriteAll(records); err != nil {
		return fmt.Errorf("failed to write records to CSV file: %v", err)
	}

	// Ensure all data is flushed to the file
	writer.Flush()

	// Check if there were any errors during flushing
	if err := writer.Error(); err != nil {
		return fmt.Errorf("error occurred while flushing data to CSV: %v", err)
	}

	fmt.Printf("Successfully saved CSV to: %s\n", filePath)
	return nil
}
