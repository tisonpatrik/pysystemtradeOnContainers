package utils

import (
	"encoding/csv"
	"encoding/json"
	"fmt"
	"io"
	"main/src/models"
	"os"
	"path/filepath"
)

// writeMergedCSV writes the final merged CSV file and adds the header.
func WriteCSVFile(filePath string, columns []string, records []models.CSVRecord) error {
	// Append the "symbol" column to the header
	file, err := os.Create(filePath)
	if err != nil {
		return err
	}
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()

	// Write the header once here
	if err := writer.Write(columns); err != nil {
		return err
	}

	// Write all records
	for _, record := range records {
		if err := writer.Write(record.Values); err != nil {
			return err
		}
	}

	return nil
}

// openCSVFile opens the CSV file for reading.
func OpenCSVFile(path, fileName string) (*os.File, error) {
	filePath := filepath.Join(path, fileName+".csv")
	file, err := os.Open(filePath)
	if err != nil {
		return nil, fmt.Errorf("failed to open file: %w", err)
	}
	return file, nil
}

// createDataDir creates the specified directory if it doesn't exist.
func CreateDir(dirPath string) error {
	if _, err := os.Stat(dirPath); os.IsNotExist(err) {
		if err := os.MkdirAll(dirPath, os.ModePerm); err != nil {
			return fmt.Errorf("cannot create directory: %v", err)
		}
	}
	return nil
}

// isDirEmpty checks if a directory is empty.
func IsDirEmpty(dirPath string) (bool, error) {
	f, err := os.Open(dirPath)
	if err != nil {
		return false, fmt.Errorf("cannot open directory: %v", err)
	}
	defer f.Close()

	_, err = f.Readdir(1)
	if err == io.EOF {
		return true, nil
	} else if err != nil {
		return false, fmt.Errorf("cannot read directory: %v", err)
	}

	return false, nil
}
func GetProjectRoot() (string, error) {
	// Get the absolute path of the executable
	executablePath, err := os.Executable()
	if err != nil {
		return "", fmt.Errorf("error determining executable path: %w", err)
	}

	// Get the directory of the executable
	executableDir := filepath.Dir(executablePath)

	// Return the parent directory of the executable's directory (which is the project root)
	projectRoot := filepath.Dir(executableDir)
	return projectRoot, nil
}

// ReadSymbolsFromCSV reads a CSV file and returns a Symbols set based on its content.
func ReadSymbolsFromCSV(filePath string) (models.Symbols, error) {
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

	// Create a Symbols set to hold unique symbols
	symbols := make(models.Symbols)

	// Populate the Symbols set from the CSV file
	for _, row := range rawRecords {
		if len(row) > 0 {
			symbol := row[0]             // Assume each row has the symbol in the first column
			symbols[symbol] = struct{}{} // Add symbol to the set
		}
	}

	return symbols, nil
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

// loadMappings loads the JSON mappings file.
func LoadJSONfile(filePath string) ([]models.Mapping, error) {
	file, err := os.Open(filePath)
	if err != nil {
		return nil, fmt.Errorf("error opening mappings JSON file: %w", err)
	}
	defer file.Close()

	var records []models.Mapping
	if err := json.NewDecoder(file).Decode(&records); err != nil {
		return nil, fmt.Errorf("error decoding mappings JSON: %w", err)
	}

	return records, nil
}

// DirExists checks if a directory exists and is indeed a directory.
func DirExists(dirPath string) (bool, error) {
	info, err := os.Stat(dirPath)
	if err != nil {
		if os.IsNotExist(err) {
			return false, nil
		}
		return false, fmt.Errorf("error checking if directory exists: %w", err)
	}

	return info.IsDir(), nil
}
