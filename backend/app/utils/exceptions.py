class RAGException(Exception):
    """
    Base exception class for RAG-related errors
    """
    def __init__(self, message: str, error_code: str = "RAG_ERROR"):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

class InvalidQueryException(RAGException):
    """
    Raised when a query is invalid or malformed
    """
    def __init__(self, message: str = "Invalid query format"):
        super().__init__(message, "INVALID_QUERY")

class ContextInsufficientException(RAGException):
    """
    Raised when there is insufficient context to answer a query
    """
    def __init__(self, message: str = "I don't know based on the provided text."):
        super().__init__(message, "CONTEXT_INSUFFICIENT")