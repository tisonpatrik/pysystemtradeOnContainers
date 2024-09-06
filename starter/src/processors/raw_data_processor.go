package processors

import "fmt"

// MultiplePricesProcessor is a placeholder for the processing logic of multiple prices.
func MultiplePricesProcessor(path string, name string, symbols [][]string, columns []string) error {
	// Implement your processing logic here
	fmt.Printf("Processing multiple prices in directory: %s\n", path)
	// Process the data as needed
	return nil
}

// FXPricesProcessor is a placeholder for the processing logic of FX prices.
func FXPricesProcessor(path string, name string, symbols [][]string, columns []string) error {
	// Implement your processing logic here
	fmt.Printf("Processing fx prices in directory: %s\n", path)
	// Process the data as needed
	return nil
}

func RollCalendarsProcessor(path string, name string, symbols [][]string, columns []string) error {
	// Implement your processing logic here
	fmt.Printf("Processing roll calendars in directory: %s\n", path)
	// Process the data as needed
	return nil
}
