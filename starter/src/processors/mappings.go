package processors

// Record represents an object with a file path and an ordered collection of column names.
type Record struct {
	Name    string   `json:"Name"`
	Path    string   `json:"Path"`
	Columns []string `json:"Columns"`
}

// Collection represents a collection of Record objects.
type Collection []Record
