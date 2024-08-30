package main

import (
	"fmt"
	"starter/src/env_generator"
	"starter/src/processors"
)

func main() {
	dirPath := "data/temp"

	fmt.Println("Welcome to the pysystemtraderOnContainers project setup!")
	fmt.Println("We have 3 tasks to complete:")
	fmt.Println("")

	fmt.Println("1. Set up environment variables.")
	fmt.Println("2. Download and process necessary data.")
	fmt.Println("3. Inject the data into the database.")

	fmt.Println("")
	fmt.Println("Let's start with the first task.")

	// Initialize environment variables and create the .env file in the project root
	if err := env_generator.SetupEnv(); err != nil {
		fmt.Println("Failed to set up environment variables:", err)
		return
	}
	if err := processors.ProcessData(dirPath); err != nil {
		fmt.Println("Failed to download and process the data:", err)
		return
	}
	// Additional steps such as injecting data into the database would go here
}
