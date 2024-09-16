package src

import (
	"bufio"
	"fmt"
	"os"
	"path/filepath"
	"strings"
)

func GetProjectRoot() (string, error) {
	// Get the absolute path of the executable
	executablePath, err := os.Executable()
	if err != nil {
		return "", fmt.Errorf("error determining executable path: %w", err)
	}

	// Get the directory of the executable
	executableDir := filepath.Dir(executablePath)

	// Get the parent directory of the executable's directory
	parentDir := filepath.Dir(executableDir)

	// Return the grandparent directory (which is two levels up from the executable)
	projectRoot := filepath.Dir(parentDir)
	return projectRoot, nil
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
