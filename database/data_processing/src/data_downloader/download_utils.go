package data_downloader

import (
	"encoding/json"
	"fmt"
	"io"
	"main/src/models"
	"net/http"
	"os"
	"path/filepath"
	"strings"
	"sync"
)

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

	var contents []models.GitHubContent
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
