import re
from .token import Token
from .patterns import LexerPatterns
from .symbol_table import SymbolTable
from .error_handler import ErrorHandler


class Lexer:
    """Main lexical analyzer"""
    
    def __init__(self):
        self.tokens = []
        self.symbol_table = SymbolTable()
        self.error_handler = ErrorHandler()
        self.patterns = LexerPatterns()
    
    def tokenize(self, source_code):
        """
        Main tokenization method
        
        Algorithm:
        1. Initialize line and column counters
        2. While there's input:
           a. Try to match each pattern
           b. If matched: create token, update position
           c. If not matched: report error
        3. Return token stream and errors
        
        Args:
            source_code (str): Raw source code to tokenize
        
        Returns:
            tuple: (tokens, errors, symbol_table)
        """
        
        # Reset for new input
        self.tokens = []
        self.symbol_table.clear()
        self.error_handler.clear()
        
        line = 1
        column = 1
        position = 0
        
        while position < len(source_code):
            char = source_code[position]
            matched = False
            

            # Try each pattern in order
            for token_type, pattern in self.patterns.PATTERNS:
                # Create regex matcher at current position
                regex = re.compile(pattern)
                match = regex.match(source_code, position)
                
                if match:
                    matched = True
                    value = match.group(0)

                    # Error-detecting patterns: report a meaningful error
                    # instead of creating a token for malformed input.
                    if token_type == 'UNTERMINATED_COMMENT':
                        self.error_handler.add_error(
                            "Unterminated block comment",
                            line,
                            column,
                            value
                       )
                    elif token_type == 'UNTERMINATED_STRING':
                        self.error_handler.add_error(
                            "Unterminated string literal (missing closing \")",
                            line, column, value
                        )
                    elif token_type == 'UNTERMINATED_CHAR':
                        self.error_handler.add_error(
                            "Unterminated character literal (missing closing ')",
                            line, column, value
                        )
                    elif token_type == 'INVALID_NUMBER':
                        self.error_handler.add_error(
                            f"Invalid number format '{value}'",
                            line, column, value
                        )
                    # Skip whitespace and comments (don't create tokens)
                    elif token_type not in ['WHITESPACE', 'COMMENT_LINE', 'COMMENT_BLOCK']:
                        # Determine final token type
                        if token_type == 'IDENTIFIER':
                            if self.patterns.is_keyword(value):
                                final_type = 'KEYWORD'
                            else:
                                final_type = 'IDENTIFIER'
                                # Add to symbol table
                                self.symbol_table.add_symbol(value, 'inferred', line, column)
                        else:
                            final_type = token_type
                        
                        # Create token
                        token = Token(final_type, value, line, column)
                        self.tokens.append(token)
                    
                    # Update position
                    for char_in_match in value:
                        if char_in_match == '\n':
                            line += 1
                            column = 1
                        else:
                            column += 1
                    
                    position = match.end()
                    break
            
            if not matched:
                # No pattern matched - lexical error!
                if self.error_handler.check_invalid_character(char):
                    self.error_handler.add_error(
                        f"Invalid character '{char}'",
                        line, column, char
                    )
                else:
                    self.error_handler.add_error(
                        f"Unexpected character '{char}'",
                        line, column, char
                    )
                
                # Move forward to recover
                if char == '\n':
                    line += 1
                    column = 1
                else:
                    column += 1
                position += 1
        
        return self.tokens, self.error_handler.get_errors(), self.symbol_table
    
    def get_tokens(self):
        """Get current token list"""
        return self.tokens
    
    def get_token_count(self):
        """Get number of tokens"""
        return len(self.tokens)
    
    def get_tokens_as_dict(self):
        """Get tokens for display (as dictionaries)"""
        return [token.to_dict() for token in self.tokens]
    
    def get_statistics(self):
        """Get tokenization statistics"""
        token_types = {}
        for token in self.tokens:
            token_types[token.type] = token_types.get(token.type, 0) + 1
        
        return {
            'Total Tokens': len(self.tokens),
            'Unique Token Types': len(token_types),
            'Token Breakdown': token_types,
            'Errors': self.error_handler.get_error_count(),
            'Symbols': len(self.symbol_table.symbols)
        }