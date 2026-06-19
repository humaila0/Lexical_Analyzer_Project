class SymbolTable:
    """Manages all identifiers found in source code"""
    
    def __init__(self):
        self.symbols = {}  # { 'name': { properties } }
    
    def add_symbol(self, name, type='inferred', line=0, column=0):
        """
        Add or update a symbol in the table
        
        Args:
            name (str): Variable/function name
            type (str): Data type (int, float, etc.) or 'inferred'
            line (int): Line number where declared
            column (int): Column number where declared
        """
        if name not in self.symbols:
            self.symbols[name] = {
                'type': type,
                'line': line,
                'column': column,
                'count': 1,  # How many times referenced
                'uses': [(line, column)]  # All places used
            }
        else:
            # Already exists, increment usage count
            self.symbols[name]['count'] += 1
            self.symbols[name]['uses'].append((line, column))
    
    def lookup(self, name):
        """
        Look up a symbol
        
        Returns:
            dict if found, None if not found
        """
        return self.symbols.get(name)
    
    def exists(self, name):
        """Check if symbol exists"""
        return name in self.symbols
    
    def get_all_symbols(self):
        """Get all symbols as list (for display)"""
        result = []
        for name, info in self.symbols.items():
            result.append({
                'Identifier': name,
                'Type': info['type'],
                'First Seen': f"Line {info['line']}, Col {info['column']}",
                'Used': info['count'],
                'Total References': len(info['uses'])
            })
        return result
    
    def clear(self):
        """Clear all symbols (for new file)"""
        self.symbols = {}