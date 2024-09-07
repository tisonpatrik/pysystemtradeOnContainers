package raw_data_processing

import (
	"fmt"
	"starter/src"
)

func MultiplePricesProcessor(input src.ProcessorInput) error {
	// Implement your processing logic here
	fmt.Printf("Processing multiple prices in directory: %s\n", input.Path)
	// Process the data as needed
	return nil
}
