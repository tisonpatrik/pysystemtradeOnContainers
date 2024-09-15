package main

import (
	"bufio"
	"fmt"
	"main/src"
	"os"
	"path/filepath"
)

func main() {

	fmt.Println("We are about to create a .env file for the database configuration.")

	// Get the project root directory
	rootPath, err := src.GetProjectRoot()
	if err != nil {
		fmt.Println("Error getting project root:", err)
		return
	}
	// Define the path for the .env file
	envFilePath := filepath.Join(rootPath, ".env")

	// Check if .env file already exists
	if src.FileExists(envFilePath) {
		reader := bufio.NewReader(os.Stdin)
		fmt.Print(".env file already exists. Do you want to overwrite it? (Y/n): ")
		overwrite, _ := reader.ReadString('\n')
		overwrite = src.TrimSpace(overwrite)

		// If the user presses Enter or types "Y/y", we proceed with overwriting
		if overwrite != "" && (overwrite != "Y" && overwrite != "y") {
			fmt.Println("Skipping .env file creation.")
			return
		}
	}

	// Initialize environment variables and create the .env file in the project root
	if err := src.SetupEnv(); err != nil {
		fmt.Println("Failed to set up environment variables:", err)
		return
	}

	fmt.Println(".env file successfully created or overwritten.")
}
