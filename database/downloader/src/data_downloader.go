package src

import (
	"fmt"
	"sync"
)

// DownloadData downloads the entire contents of the GitHub directory into the specified local directory "data/temp".
func DownloadData(dirPath string) error {

	// Ensure the directory exists
	fmt.Printf("Creating directory %s\n", dirPath)
	if err := createDir(dirPath); err != nil {
		return err
	}

	// Start downloading data from GitHub
	baseURL := "https://api.github.com/repos/tisonpatrik/pysystemtrade_preprocessing/contents/data"
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
