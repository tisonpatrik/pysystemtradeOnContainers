package raw_data_processing

import (
	"fmt"
	"starter/src"
)

func FXPricesProcessor(input src.ProcessorInput) error {
	// Implement your processing logic here
	fmt.Printf("Processing fx prices in directory: %s\n", input.Path)
	// Process the data as needed
	return nil
}
