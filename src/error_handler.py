class LexicalError:
    """Represents a lexical error"""
    
    def __init__(self, message, line, column, char=None):
        self.message = message
        self.line = line
        self.column = column
        self.char = char or ''
    
    def __str__(self):
        return f"Error at Line {self.line}, Column {self.column}: {self.message}"
    
    def to_dict(self):
        return {
            'Line': self.line,
            'Column': self.column,
            'Error': self.message,
            'Character': self.char
        }


class ErrorHandler:
    """Detect and report lexical errors"""
    
    def __init__(self):
        self.errors = []
    
    def add_error(self, message, line, column, char=None):
        """Add an error to the error list"""
        error = LexicalError(message, line, column, char)
        self.errors.append(error)
    
    def check_unterminated_string(self, text, start_pos, line, col):
        """Check for unterminated string literal"""
        if '"' in text[start_pos:]:
            return False
        return True
    
    def check_unterminated_comment(self, text, start_pos, line, col):
        """Check for unterminated block comment"""
        if '*/' not in text[start_pos:]:
            return True
        return False
    
    def check_invalid_character(self, char):
        """Check if character is valid"""
        # Valid characters: letters, digits, symbols, whitespace
        if ord(char) < 32 and char not in '\n\t\r':
            return True  # Invalid
        return False
    
    def get_errors(self):
        """Get all errors"""
        return self.errors
    
    def get_error_count(self):
        """Get number of errors"""
        return len(self.errors)
    
    def has_errors(self):
        """Check if any errors"""
        return len(self.errors) > 0
    
    def clear(self):
        """Clear all errors"""
        self.errors = []
    
    def get_errors_as_dict(self):
        """Get errors for display"""
        return [error.to_dict() for error in self.errors]