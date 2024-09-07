package utils

import (
	"bufio"
	"encoding/csv"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"starter/src"
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

// ReadCSVFile reads a CSV file and returns its contents.
func ReadCSVFile(filePath string) ([]src.CSVRecord, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, fmt.Errorf("could not open the file: %v", err)
	}
	defer file.Close()

	reader := csv.NewReader(file)
	rawRecords, err := reader.ReadAll()
	if err != nil {
		return nil, fmt.Errorf("could not read the CSV file: %v", err)
	}

	if len(rawRecords) == 0 {
		return nil, fmt.Errorf("the CSV file is empty")
	}

	// First row is the header (columns)
	columns := rawRecords[0]

	// Rest of the rows are data
	var records []src.CSVRecord
	for _, row := range rawRecords[1:] {
		record := src.CSVRecord{
			Columns: columns, // Header (columns) stays the same for all records
			Values:  row,     // Values from the CSV row
		}
		records = append(records, record)
	}

	return records, nil
}

// GetCSVFiles returns a list of all CSV files in the specified directory.
func GetCSVFiles(dir string) ([]string, error) {
	files, err := os.ReadDir(dir)
	if err != nil {
		return nil, fmt.Errorf("error reading directory: %w", err)
	}

	var csvFiles []string
	for _, file := range files {
		if !file.IsDir() && filepath.Ext(file.Name()) == ".csv" {
			csvFiles = append(csvFiles, file.Name())
		}
	}

	return csvFiles, nil
}

// SaveRecordsToCSV saves records to a CSV file.
func SaveRecordsToCSV(directory string, filename string, records []src.CSVRecord) error {
	// Create the directory if it doesn't exist
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

	// Create a CSV writer
	writer := csv.NewWriter(file)

	// Write the header row (columns)
	if len(records) > 0 {
		if err := writer.Write(records[0].Columns); err != nil {
			return fmt.Errorf("failed to write CSV header: %v", err)
		}
	}

	// Write the data rows (values)
	for _, record := range records {
		if err := writer.Write(record.Values); err != nil {
			return fmt.Errorf("failed to write CSV row: %v", err)
		}
	}

	// Flush the writer
	writer.Flush()

	// Check for any error during flush
	if err := writer.Error(); err != nil {
		return fmt.Errorf("error occurred while flushing data to CSV: %v", err)
	}

	fmt.Printf("Successfully saved CSV to: %s\n", filePath)
	return nil
}

// loadMappings loads the JSON mappings file.
func LoadJSONfile(filePath string) ([]src.Mapping, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, fmt.Errorf("error opening mappings JSON file: %w", err)
	}
	defer file.Close()

	var records []src.Mapping
	if err := json.NewDecoder(file).Decode(&records); err != nil {
		return nil, fmt.Errorf("error decoding mappings JSON: %w", err)
	}

	return records, nil
}
