package processors

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

// DownloadData downloads the entire contents of the GitHub directory into the specified local directory and returns a list of downloaded or existing subdirectories.
func DownloadData(dirPath string) ([]string, error) {
	// Ensure the directory exists
	err := createDataDir(dirPath)
	if err != nil {
		return nil, err
	}

	// Check if the directory is empty
	isEmpty, err := isDirEmpty(dirPath)
	if err != nil {
		return nil, err
	}

	var wg sync.WaitGroup
	errors := make(chan error, 10)
	subdirectories := make(chan string, 10) // Channel to collect successfully downloaded or existing subdirectories

	// If the directory is empty, download the data
	if isEmpty {
		baseURL := "https://api.github.com/repos/tisonpatrik/pysystemtrade/contents/data/futures"
		rootDir := "data/futures" // This is the part of the path we want to strip

		wg.Add(1)
		go downloadDirectory(baseURL, dirPath, rootDir, &wg, errors, subdirectories)
	} else {
		// If not empty, gather existing subdirectories
		err := filepath.Walk(dirPath, func(path string, info os.FileInfo, err error) error {
			if err != nil {
				return err
			}
			if info.IsDir() && path != dirPath {
				subdirectories <- path
			}
			return nil
		})
		if err != nil {
			return nil, err
		}
	}

	go func() {
		wg.Wait()
		close(errors)
		close(subdirectories)
	}()

	var downloadedDirs []string
	for dir := range subdirectories {
		downloadedDirs = append(downloadedDirs, dir)
	}

	for err := range errors {
		if err != nil {
			return nil, fmt.Errorf("download encountered an error: %v", err)
		}
	}

	return downloadedDirs, nil
}

// createDataDir creates the specified directory if it doesn't exist.
func createDataDir(dirPath string) error {
	if _, err := os.Stat(dirPath); os.IsNotExist(err) {
		err := os.MkdirAll(dirPath, os.ModePerm)
		if err != nil {
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

// downloadDirectory recursively downloads a directory from the GitHub repository and records the subdirectory names.
func downloadDirectory(baseURL, localDir, rootDir string, wg *sync.WaitGroup, errors chan<- error, subdirectories chan<- string) {
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
		// Adjust the localPath to strip the root directory part from the GitHub path
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
			subdirectories <- localPath // Record the successfully created subdirectory
			wg.Add(1)
			dirURL := baseURL + "/" + item.Name
			go downloadDirectory(dirURL, localDir, rootDir, wg, errors, subdirectories)
		}
	}
}
