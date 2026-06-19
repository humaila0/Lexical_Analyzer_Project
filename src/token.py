class Token:
    """Represents a single token in the source code"""
    
    def __init__(self, type, value, line, column):
        """
        Initialize a token
        
        Args:
            type (str): Token type (KEYWORD, IDENTIFIER, NUMBER, etc.)
            value (str): The actual text of the token
            line (int): Line number where token appears
            column (int): Column number where token starts
        """
        self.type = type
        self.value = value
        self.line = line
        self.column = column
    
    def __repr__(self):
        """String representation for debugging"""
        return f"Token({self.type}, '{self.value}', {self.line}, {self.column})"
    
    def __str__(self):
        """Pretty print"""
        return f"{self.type:15} {self.value:20} Line {self.line:3} Col {self.column:3}"
    
    def to_dict(self):
        """Convert to dictionary (useful for displaying in GUI)"""
        return {
            'Type': self.type,
            'Value': self.value,
            'Line': self.line,
            'Column': self.column
        }