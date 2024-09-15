package src

import (
	"fmt"
	"path/filepath"
	"strconv"
)

// SetupEnv initializes environment variables and writes them to the .env file in the project root directory.
func SetupEnv() error {
	envVariables := getEnvVariables()

	// Get the project root directory
	rootPath, err := GetProjectRoot()
	if err != nil {
		return fmt.Errorf("error determining project root path: %w", err)
	}

	envFilePath := filepath.Join(rootPath, ".env")

	// Create the .env file with environment variables
	if err := createEnvFile(envVariables, envFilePath); err != nil {
		return err
	}

	fmt.Printf(".env file created successfully at: %s\n", envFilePath)
	return nil
}

// getEnvVariables prompts the user for all required environment variables and returns them as a map.
func getEnvVariables() map[string]string {
	return map[string]string{
		"DB_NAME":     promptEnvVariable("DB_NAME", "database"),
		"DB_USER":     promptEnvVariable("DB_USER", "postgres"),
		"DB_PASSWORD": promptEnvVariable("DB_PASSWORD", "postgres"),
		"DB_HOST":     promptEnvVariable("DB_HOST", "postgres"),
		"DB_PORT":     promptEnvVariableInt("DB_PORT", 5432),
		"DB_SSLMODE":  promptDBSSLMode(),
	}
}

// createEnvFile creates a .env file in the specified directory and writes the environment variables to it.
func createEnvFile(envVariables map[string]string, envFilePath string) error {
	file, err := CreateFile(envFilePath)
	if err != nil {
		return fmt.Errorf("error creating .env file: %w", err)
	}
	defer file.Close()

	for key, value := range envVariables {
		_, err := file.WriteString(fmt.Sprintf("%s=%s\n", key, value))
		if err != nil {
			return fmt.Errorf("error writing to .env file: %w", err)
		}
	}

	return nil
}

// promptEnvVariable prompts the user for an environment variable value and returns it.
// The user can press Enter to accept the default value.
func promptEnvVariable(name, defaultValue string) string {
	reader := GetReader()
	fmt.Printf("Enter value for %s [%s] (press Enter to keep default): ", name, defaultValue)
	value, _ := reader.ReadString('\n')
	value = TrimSpace(value)
	if value == "" {
		return defaultValue
	}
	return value
}

// promptEnvVariableInt prompts the user for an integer environment variable value and returns it as a string.
// The user can press Enter to accept the default value. If the input is not an integer, the user is prompted again.
func promptEnvVariableInt(name string, defaultValue int) string {
	reader := GetReader()
	for {
		fmt.Printf("Enter value for %s [%d] (press Enter to keep default): ", name, defaultValue)
		value, _ := reader.ReadString('\n')
		value = TrimSpace(value)
		if value == "" {
			return strconv.Itoa(defaultValue)
		}
		if _, err := strconv.Atoi(value); err == nil {
			return value
		}
		fmt.Println("Invalid input. Please enter a valid integer.")
	}
}

// promptDBSSLMode prompts the user to choose from the available DB_SSLMODE options with descriptions.
func promptDBSSLMode() string {
	sslModes := map[string]string{
		"disable":     "No SSL. I don't care about security and don't want the overhead of encryption.",
		"allow":       "Maybe encrypted. I don't care about security, but will allow encryption if the server insists.",
		"prefer":      "Maybe encrypted. I don't care about encryption, but prefer it if the server supports it.",
		"require":     "Encrypted. I want my data encrypted and trust that the server is the right one.",
		"verify-ca":   "Encrypted. I want my data encrypted and verify the server's certificate authority.",
		"verify-full": "Encrypted. I want encryption and to ensure I connect to the server I specify, verified fully.",
	}

	// Create a list of the keys to display options in a consistent order
	options := []string{"disable", "allow", "prefer", "require", "verify-ca", "verify-full"}

	reader := GetReader()
	fmt.Println("Choose an SSL mode for DB_SSLMODE:")
	for i, option := range options {
		fmt.Printf("%d. %s - %s\n", i+1, option, sslModes[option])
	}

	for {
		fmt.Print("Enter your choice (press Enter to default to 'disable'): ")
		value, _ := reader.ReadString('\n')
		value = TrimSpace(value)

		// Default to "disable" if Enter is pressed without input
		if value == "" {
			return "disable"
		}

		// Convert input to an integer and validate the range
		if choice, err := strconv.Atoi(value); err == nil && choice > 0 && choice <= len(options) {
			return options[choice-1]
		}

		fmt.Println("Invalid choice. Please enter a valid number.")
	}
}
