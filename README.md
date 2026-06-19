# Lexical Analyzer

## Overview

This is a **lexical analyzer** (lexer/scanner) that demonstrates the first phase of compiler construction. It converts raw C source code into a stream of tokens, manages a symbol table of identifiers, and detects lexical errors with clear, line/column-accurate messages.

## Features

- ✅ **Tokenization** - Converts source code into tokens
- ✅ **Symbol Table** - Tracks all identifiers found
- ✅ **Error Detection** - Identifies lexical errors with line/column info
- ✅ **GUI Interface** - User-friendly Streamlit application
- ✅ **File Upload** - Supports uploading `.c` files
- ✅ **Statistics** - Shows token breakdown and analysis
- ✅ **Download Results** - Export tokens and symbol table as CSV

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/humaila0/Lexical_Analyzer_Project.git
cd Lexical_Analyzer_Project
```

### 2. Install Python (if not already installed)

- Download from https://www.python.org/downloads/
- Choose Python 3.8 or higher

### 3. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
streamlit run gui/app.py
```

The application will open in your browser at `http://localhost:8501`

## Project Structure

```
lexical_analyzer_pro/
├── src/
│   ├── __init__.py
│   ├── token.py              # Token class
│   ├── lexer.py               # Main lexer engine
│   ├── symbol_table.py       # Symbol table
│   ├── error_handler.py      # Error detection
│   └── patterns.py            # Token patterns
├── gui/
│   └── app.py                 # Streamlit GUI
├── samples/
│   ├── sample1.c              # Simple, valid example
│   ├── sample2.c              # Invalid character + malformed number
│   ├── sample3.c              # Complex, realistic example (struct, loops)
│   └── sample4.c              # Stress test: 5 error types in one file
├── README.md                  # This file
├── requirements.txt           # Dependencies
└── .gitignore
```

## How to Use

### 1. Paste Code Directly

- Paste C code into the text area
- Click "🚀 Analyze Code"
- View results

### 2. Upload File

- Click "Upload File"
- Select a `.c` or `.txt` file
- Results appear automatically

### 3. View Results

- **Tokens** - All tokens with line/column numbers
- **Symbol Table** - All identifiers found
- **Errors** - Any lexical errors detected
- **Statistics** - Breakdown of token types

### 4. Download Results

- Click "📥 Download Tokens (CSV)" to save tokens
- Click "📥 Download Symbol Table (CSV)" to save symbols

## Supported Token Types

- **Keywords**: int, float, void, if, else, while, for, return, etc.
- **Identifiers**: Variable and function names
- **Numbers**: Integers (42) and floats (3.14)
- **Operators**: +, -, \*, /, =, ==, !=, <=, >=, &&, ||, etc.
- **Delimiters**: {, }, (, ), [, ], ;, :, ,
- **Strings**: "text" with escape sequences
- **Characters**: 'a' with escape sequences
- **Comments**: // line comments and /\* block comments \*/

## Error Detection

The analyzer detects:

- Invalid / unexpected characters (e.g. `@`, `?`)
- Unterminated string literals (e.g. `"hello;` with no closing quote)
- Unterminated character literals
- Unterminated block comments (e.g. `/* comment` with no closing `*/`)
- Malformed number formats (e.g. `0..75`, `123abc`)

Each error shows:

- Line number
- Column number
- A clear, specific message (e.g. "Unterminated string literal", "Invalid number format '0..75'")
- The character or text that caused it

**Note on scope:** preprocessor directives such as `#include` are intentionally not handled, since they fall outside the lexical rules of this C subset. Likewise, missing semicolons, unmatched braces, and type errors are not flagged here — those are syntax/semantic errors, handled by later compiler phases, not by the lexer.

## Example

### Input

```c
int x = 10;
y = x + 20;
```

### Output (Tokens)

```
Type       Value   Line  Column
KEYWORD    int     1     1
IDENTIFIER x       1     5
OPERATOR   =       1     7
NUMBER     10      1     9
DELIMITER  ;       1     11
IDENTIFIER y       2     1
OPERATOR   =       2     3
IDENTIFIER x       2     5
OPERATOR   +       2     7
NUMBER     20      2     9
DELIMITER  ;       2     11
```

### Symbol Table

```
Identifier  Type      First Seen       Used
x           inferred  Line 1, Col 5    2
y           inferred  Line 2, Col 1    1
```

## How It Works

### Tokenization Algorithm

1. Read source code character by character
2. Try to match each pattern (in priority order)
3. When pattern matches:
   - If it is an error-detecting pattern (unterminated string/char/comment, malformed number), report a descriptive error instead of creating a token
   - Otherwise create a token, record its position (line/column), and add it to the symbol table if it's an identifier
4. If no pattern matches:
   - Report an invalid/unexpected character error
   - Skip the character and keep scanning (error recovery, so multiple errors in one file are all reported)
5. Repeat until end of file

### Pattern Matching Order

Order matters! The lexer always takes the _first_ pattern that matches at a position, so patterns are checked in this priority:

1. Comments (`//` and `/* */`)
2. Error-detecting patterns (unterminated comment, unterminated string/char, malformed number) — checked _before_ their "valid" counterparts, so broken input is caught before a looser pattern can match only a fragment of it
3. Strings (`"…"`) and characters (`'…'`)
4. Numbers (`123`, `3.14`, `0xFF`)
5. Identifiers and keywords
6. Operators (`+`, `-`, `==`, etc. — longest match first)
7. Delimiters (`{`, `}`, `;`, etc.)
8. Whitespace (skipped)

## Testing

Use the provided sample files in the GUI to test the lexer's capabilities:

1. **sample1.c** - Simple, fully valid code (0 errors expected)
2. **sample2.c** - Invalid character (`?`) and malformed number (`123abc`)
3. **sample3.c** - Complex, realistic code (struct, typedef, for/while loops)
4. **sample4.c** - Stress test covering 5 different error types in one file

Upload these files in the GUI, or paste them directly into the text area.

## Troubleshooting

### Issue: "streamlit command not found"

**Solution**: Make sure virtual environment is activated

```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### Issue: "ModuleNotFoundError: No module named 'streamlit'"

**Solution**: Install dependencies

```bash
pip install -r requirements.txt
```

### Issue: "ModuleNotFoundError: No module named 'src'"

**Solution**: Run the app from the project root folder (the one containing both `src/` and `gui/`), not from inside `gui/`:

```bash
cd lexical_analyzer_pro
streamlit run gui/app.py
```

### Issue: Port 8501 already in use

**Solution**: Use a different port

```bash
streamlit run gui/app.py --server.port 8502
```

## Compiler Phases

This lexical analyzer represents the **first phase**:

```
Source Code
    ↓
[LEXICAL ANALYSIS] ← YOU ARE HERE
    ↓
Token Stream
    ↓
[SYNTAX ANALYSIS]
    ↓
Parse Tree
    ↓
[SEMANTIC ANALYSIS]
    ↓
Intermediate Code
    ↓
[CODE GENERATION]
    ↓
Machine Code
```
