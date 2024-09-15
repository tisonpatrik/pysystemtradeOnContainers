package src

import (
	"fmt"
	"os"
	"path/filepath"
)

// DeleteTempDirectory removes the temporary directory at the specified root path.
func DeleteTempDirectory(rootPath string) error {
	// Build the full path to the temp directory
	tempDir := filepath.Join(rootPath, "data", "temp")

	// Check if the temp directory exists
	if _, err := os.Stat(tempDir); os.IsNotExist(err) {
		return fmt.Errorf("temp directory does not exist: %s", tempDir)
	}

	// Attempt to remove the directory and all its contents
	if err := os.RemoveAll(tempDir); err != nil {
		return fmt.Errorf("failed to delete temp directory: %v", err)
	}

	fmt.Println("Temporary directory successfully deleted:", tempDir)
	return nil
}
