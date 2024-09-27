package src

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"sync"
)

// createDataDir creates the specified directory if it doesn't exist.
func createDir(dirPath string) error {
	if _, err := os.Stat(dirPath); os.IsNotExist(err) {
		if err := os.MkdirAll(dirPath, os.ModePerm); err != nil {
			return fmt.Errorf("cannot create directory: %v", err)
		}
	}
	return nil
}

// IsDirEmpty checks if a directory is empty.
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

// downloadFile downloads a file from the specified URL and saves it to the given path.
func downloadFile(url, filePath string, wg *sync.WaitGroup, errors chan<- error) {
	defer wg.Done()

	resp, err := http.Get(url)
	if err != nil {
		errors <- fmt.Errorf("cannot download file: %v", err)
		return
	}
	defer resp.Body.Close()

	out, err := os.Create(filePath)
	if err != nil {
		errors <- fmt.Errorf("cannot create file: %v", err)
		return
	}
	defer out.Close()

	_, err = io.Copy(out, resp.Body)
	if err != nil {
		errors <- fmt.Errorf("cannot save file: %v", err)
		return
	}
}

// downloadDirectory recursively downloads a directory from the GitHub repository.
func downloadDirectory(baseURL, localDir, rootDir string, wg *sync.WaitGroup, errors chan<- error) {
	defer wg.Done()

	resp, err := http.Get(baseURL)
	if err != nil {
		errors <- fmt.Errorf("cannot access GitHub API: %v", err)
		return
	}
	defer resp.Body.Close()

	var contents []GitHubContent
	if err := json.NewDecoder(resp.Body).Decode(&contents); err != nil {
		errors <- fmt.Errorf("cannot decode response: %v", err)
		return
	}

	for _, item := range contents {
		relativePath := strings.TrimPrefix(item.Path, rootDir)
		localPath := filepath.Join(localDir, relativePath)

		if item.Type == "file" {
			wg.Add(1)
			fileURL := "https://raw.githubusercontent.com/tisonpatrik/pysystemtrade/master/" + item.Path
			go downloadFile(fileURL, localPath, wg, errors)
		} else if item.Type == "dir" {
			if err := os.MkdirAll(localPath, os.ModePerm); err != nil {
				errors <- fmt.Errorf("cannot create directory: %v", err)
				return
			}
			wg.Add(1)
			dirURL := baseURL + "/" + item.Name
			go downloadDirectory(dirURL, localDir, rootDir, wg, errors)
		}
	}
}

// IsDirExists checks if a directory exists and is indeed a directory.
func IsDirExists(dirPath string) (bool, error) {
	info, err := os.Stat(dirPath)
	if err != nil {
		if os.IsNotExist(err) {
			return false, nil
		}
		return false, fmt.Errorf("error checking if directory exists: %w", err)
	}

	return info.IsDir(), nil
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
