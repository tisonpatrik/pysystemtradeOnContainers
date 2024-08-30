package processors

// GitHubContent represents a single item (file or directory) in a GitHub repository.
type GitHubContent struct {
	Name string `json:"name"`
	Path string `json:"path"`
	Type string `json:"type"`
}
