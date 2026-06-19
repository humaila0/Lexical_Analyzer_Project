import re

class LexerPatterns:
    """Define all token patterns for C language"""
    
    # Keywords in C
    KEYWORDS = {
        'auto', 'break', 'case', 'char', 'const', 'continue',
        'default', 'do', 'double', 'else', 'enum', 'extern',
        'float', 'for', 'goto', 'if', 'inline', 'int',
        'long', 'register', 'restrict', 'return', 'short',
        'signed', 'sizeof', 'static', 'struct', 'switch',
        'typedef', 'union', 'unsigned', 'void', 'volatile',
        'while'
    }
    
    # Token patterns (order matters! More specific first)
    PATTERNS = [
        # Comments (must be before operators because of /)
        ('COMMENT_LINE', r'//.*'),
        ('UNTERMINATED_COMMENT', r'/\*[\s\S]*\Z'),
        ('COMMENT_BLOCK', r'/\*[\s\S]*?\*/'),

        # --- Error-detecting patterns: must come BEFORE the "valid" versions
        # below, otherwise the valid patterns will match a partial fragment
        # and the malformed input slips through with no error. ---

        # Unterminated string: opening quote with no matching closing quote
        # before end of line. Must be checked before STRING.
        ('UNTERMINATED_STRING', r'"([^"\\\n]|\\.)*(?=\n|\Z)'),

        # Unterminated character literal (same idea as above, for ' ').
        ('UNTERMINATED_CHAR', r"'([^'\\\n]|\\.)*(?=\n|\Z)"),

        # Malformed number: digits, a dot, then another dot or a letter
        # (e.g. 0..75, 3.14.15, 12.5e, 123abc). Must be checked before
        # NUMBER/IDENTIFIER so it "wins" the match at that position.
        ('INVALID_NUMBER', r'\d+\.\d*\.\d*|\d+\.\d+[a-zA-Z_]\w*|\d+[a-zA-Z_]\w*'),

        # Strings and characters (must be before operators because of quotes)
        ('STRING', r'"([^"\\]|\\.)*"'),
        ('CHAR', r"'([^'\\]|\\.)'"),
        
        # Numbers (must be before operators because of .)
        ('NUMBER', r'\b\d+(\.\d+)?([eE][+-]?\d+)?\b'),
        ('HEX_NUMBER', r'0[xX][0-9a-fA-F]+'),
        
        # Identifiers and keywords (must be checked for keywords)
        ('IDENTIFIER', r'[a-zA-Z_]\w*'),
        
        # Operators (longer operators first: == before =)
        ('OPERATOR', r'(==|!=|<=|>=|\+\+|--|\-\>|&&|\|\||<<|>>|\+=|\-=|\*=|/=|%=|&=|\|=|\^=|<<=|>>=|[+\-*/%=<>!&|^~])'),
        
        # Delimiters
        ('DELIMITER', r'[(){}\[\];:,.]'),
        
        # Whitespace (space, tab, newline)
        ('WHITESPACE', r'[ \t]+'),
        ('NEWLINE', r'\n'),
    ]
    
    @staticmethod
    def is_keyword(word):
        """Check if word is a C keyword"""
        return word in LexerPatterns.KEYWORDS