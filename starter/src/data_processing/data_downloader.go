package data_processing

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"
	"starter/src"
	"strings"
	"sync"
)

// DownloadData downloads the entire contents of the GitHub directory into the specified local directory.
func DownloadData(dirPath string) error {
	// Ensure the directory exists
	if err := createDataDir(dirPath); err != nil {
		return err
	}

	// Check if the directory is empty
	isEmpty, err := isDirEmpty(dirPath)
	if err != nil {
		return err
	}

	// If the directory is not empty, no need to download again
	if !isEmpty {
		fmt.Printf("Directory %s is not empty, skipping download.\n", dirPath)
		return nil
	}

	// Start downloading data from GitHub
	baseURL := "https://api.github.com/repos/tisonpatrik/pysystemtrade/contents/data/futures"
	rootDir := "data/futures" // This is the part of the path we want to strip

	var wg sync.WaitGroup
	errors := make(chan error, 10)

	wg.Add(1)
	go downloadDirectory(baseURL, dirPath, rootDir, &wg, errors)

	// Wait for all downloads to complete
	go func() {
		wg.Wait()
		close(errors)
	}()

	// Check for any errors that occurred during download
	for err := range errors {
		if err != nil {
			return fmt.Errorf("download encountered an error: %v", err)
		}
	}

	return nil
}

// createDataDir creates the specified directory if it doesn't exist.
func createDataDir(dirPath string) error {
	if _, err := os.Stat(dirPath); os.IsNotExist(err) {
		if err := os.MkdirAll(dirPath, os.ModePerm); err != nil {
			return fmt.Errorf("cannot create directory: %v", err)
		}
	}
	return nil
}

// isDirEmpty checks if a directory is empty.
func isDirEmpty(dirPath string) (bool, error) {
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

	fmt.Printf("Downloaded: %s\n", filePath)
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

	var contents []src.GitHubContent
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
