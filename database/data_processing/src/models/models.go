package models

// Define a type for processor functions
type ProcessorFunc func(ProcessorInput) error

// Mapping represents an object with a file path and an ordered collection of column names.
type Mapping struct {
	Name    string   `json:"Name"`
	Path    string   `json:"Path"`
	Columns []string `json:"Columns"`
}

// Struct for input to processor functions
type ProcessorInput struct {
	Path            string
	Name            string
	Symbols         []CSVRecord
	NewColumnsNames []string
}

// CSVRecord represents a row in the CSV file.
type CSVRecord struct {
	Columns []string
	Values  []string
}

// DataFrame represents the data from a CSV file.
type DataFrame struct {
	SymbolName string
	Records    []CSVRecord
}

type GitHubContent struct {
	Name string `json:"name"`
	Path string `json:"path"`
	Type string `json:"type"`
}
