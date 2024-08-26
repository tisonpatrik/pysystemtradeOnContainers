package main

import (
	"fmt"
	processes "starter/processes"
)

func main() {
	fmt.Println("Welcome to the pysystemtraderOnContainers project setup!")
	fmt.Println("We have 3 tasks to complete:")
	fmt.Println("")

	fmt.Println("1. Set up environment variables.")
	fmt.Println("2. Download and clean the data.")
	fmt.Println("3. Inject the data into the database.")

	fmt.Println("")
	fmt.Println("Let's start with the first task.")

	// Initialize environment variables and create the .env file in the project root
	if err := processes.SetupEnv(); err != nil {
		fmt.Println("Failed to set up environment variables:", err)
		return
	}
	if err := processes.DownloadData(); err != nil {
		fmt.Println("Failed to download and clean the data:", err)
		return
	}
	// Additional steps such as downloading data and injecting into the database would go here
}
