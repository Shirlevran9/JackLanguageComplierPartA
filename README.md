# Jack Language Compiler - Part A

This project implements the first part of the Jack language compiler as part of the nand2tetris course. The implementation includes:

## Components

1. **JackTokenizer**: A lexical analyzer that breaks Jack source code into tokens according to the Jack language specification.
   - Handles keywords, symbols, identifiers, integer constants, and string constants
   - Supports special XML character escaping for symbols (<, >, &)
   - Implements unary operators (^ for left-shift and # for right-shift)

## Features

- Tokenizes Jack source code into XML format
- Handles all Jack language lexical elements
- Supports comments removal (//, /* */, /** */)
- Proper XML escaping for special characters
- Comprehensive test suite

## Usage

```bash
python JackTokenizerTest.py <input_file.jack> <output_file.xml>
```

## Testing

The project includes test cases for:
- Basic Jack language constructs
- Special symbols and operators
- String constants
- Comments
- Unary operators (^ and #) 