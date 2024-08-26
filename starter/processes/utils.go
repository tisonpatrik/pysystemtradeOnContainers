package processes

import (
	"bufio"
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
