class HttpClientError(Exception):
    """Base class for all HTTP client errors."""


class HttpStatusError(HttpClientError):
    """Error related to an unsuccessful HTTP status code."""

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        super().__init__(f"HTTP Status {status_code}: {message}")


class HttpRequestError(HttpClientError):
    """Error related to the request (e.g., network issues)."""

    def __init__(self, url: str, message: str):
        self.url = url
        super().__init__(f"Request to {url} failed: {message}")


class HttpUnexpectedError(HttpClientError):
    """General unexpected error during an HTTP request."""

    def __init__(self, message: str):
        super().__init__(f"Unexpected error: {message}")
