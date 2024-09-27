package main

import (
	"fmt"
	"os"
	"path/filepath"
)

func main() {
	rootPath, err := GetProjectRoot()
	if err != nil {
		fmt.Println("Error getting project root:", err)
		return
	}

	// Build the full path to the temp directory
	tempDir := filepath.Join(rootPath, "data", "temp")

	// Check if the temp directory exists
	if _, err := os.Stat(tempDir); os.IsNotExist(err) {
		fmt.Printf("temp directory does not exist: %s\n", tempDir)
		return
	}

	// Attempt to remove the directory and all its contents
	if err := os.RemoveAll(tempDir); err != nil {
		fmt.Printf("failed to delete temp directory: %v\n", err)
		return
	}

	fmt.Println("Temporary directory successfully deleted:", tempDir)
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
