package data_downloader

import (
	"fmt"
	"main/src/utils"
	"path/filepath"
	"sync"
)

// DownloadData downloads the entire contents of the GitHub directory into the specified local directory "data/temp".
func DownloadData(dirPath string) error {
	// Construct the full path for the download directory as "dirPath/data/temp"
	downloadDir := filepath.Join(dirPath, "data", "temp")

	// Ensure the directory exists
	fmt.Printf("Creating directory %s\n", downloadDir)
	if err := utils.CreateDir(downloadDir); err != nil {
		return err
	}

	// Check if the directory is empty
	isEmpty, err := utils.IsDirEmpty(downloadDir)
	if err != nil {
		return err
	}

	// If the directory is not empty, no need to download again
	if !isEmpty {
		fmt.Printf("Directory %s is not empty, skipping download.\n", downloadDir)
		return nil
	}

	// Start downloading data from GitHub
	baseURL := "https://api.github.com/repos/tisonpatrik/pysystemtrade/contents/data/futures"
	rootDir := "data/futures" // This is the part of the path we want to strip

	var wg sync.WaitGroup
	errors := make(chan error, 10)

	wg.Add(1)
	go downloadDirectory(baseURL, downloadDir, rootDir, &wg, errors)

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
