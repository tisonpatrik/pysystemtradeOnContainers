package processes

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

// DownloadData downloads the entire contents of the GitHub directory into the local "data/temp" directory.
func DownloadData() error {
	dirPath := "data/temp"

	// Check if the directory exists and is not empty
	if _, err := os.Stat(dirPath); err == nil {
		isEmpty, err := isDirEmpty(dirPath)
		if err != nil {
			return err
		}
		if !isEmpty {
			fmt.Println("Directory already exists and is not empty. Skipping download.")
			return nil
		}
	}

	err := createDataDir()
	if err != nil {
		return err
	}

	baseURL := "https://api.github.com/repos/tisonpatrik/pysystemtrade/contents/data/futures"
	localDir := "data/temp"
	rootDir := "data/futures" // This is the part of the path we want to strip

	var wg sync.WaitGroup
	errors := make(chan error, 10)

	wg.Add(1)
	go downloadDirectory(baseURL, localDir, rootDir, &wg, errors)

	go func() {
		wg.Wait()
		close(errors)
	}()

	for err := range errors {
		if err != nil {
			return fmt.Errorf("download encountered an error: %v", err)
		}
	}

	return nil
}
// createDataDir creates the "data/temp" directory in the project root.
func createDataDir() error {
	dirPath := "data/temp"
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
			wg.Add(1)
			dirURL := baseURL + "/" + item.Name
			go downloadDirectory(dirURL, localDir, rootDir, wg, errors)
		}
	}
}
