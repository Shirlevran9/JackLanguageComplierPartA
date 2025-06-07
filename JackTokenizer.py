"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""
import typing
import re
from Constants import *

class JackTokenizer:
    """Removes all comments from the input stream and breaks it
    into Jack language tokens, as specified by the Jack grammar.
    
    # Jack Language Grammar

    A Jack file is a stream of characters. If the file represents a
    valid program, it can be tokenized into a stream of valid tokens. The
    tokens may be separated by an arbitrary number of whitespace characters, 
    and comments, which are ignored. There are three possible comment formats: 
    /* comment until closing */ , /** API comment until closing */ , and 
    // comment until the line's end.

    - 'xxx': quotes are used for tokens that appear verbatim (terminals).
    - xxx: regular typeface is used for names of language constructs 
           (non-terminals).
    - (): parentheses are used for grouping of language constructs.
    - x | y: indicates that either x or y can appear.
    - x?: indicates that x appears 0 or 1 times.
    - x*: indicates that x appears 0 or more times.

    ## Lexical Elements

    The Jack language includes five types of terminal elements (tokens).

    - keyword: 'class' | 'constructor' | 'function' | 'method' | 'field' | 
               'static' | 'var' | 'int' | 'char' | 'boolean' | 'void' | 'true' |
               'false' | 'null' | 'this' | 'let' | 'do' | 'if' | 'else' | 
               'while' | 'return'
    - symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' | 
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
    - integerConstant: A decimal number in the range 0-32767.
    - StringConstant: '"' A sequence of Unicode characters not including 
                      double quote or newline '"'
    - identifier: A sequence of letters, digits, and underscore ('_') not 
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.

    ## Program Structure

    A Jack program is a collection of classes, each appearing in a separate 
    file. A compilation unit is a single class. A class is a sequence of tokens 
    structured according to the following context free syntax:
    
    - class: 'class' className '{' classVarDec* subroutineDec* '}'
    - classVarDec: ('static' | 'field') type varName (',' varName)* ';'
    - type: 'int' | 'char' | 'boolean' | className
    - subroutineDec: ('constructor' | 'function' | 'method') ('void' | type) 
    - subroutineName '(' parameterList ')' subroutineBody
    - parameterList: ((type varName) (',' type varName)*)?
    - subroutineBody: '{' varDec* statements '}'
    - varDec: 'var' type varName (',' varName)* ';'
    - className: identifier
    - subroutineName: identifier
    - varName: identifier

    ## Statements

    - statements: statement*
    - statement: letStatement | ifStatement | whileStatement | doStatement | 
                 returnStatement
    - letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
    - ifStatement: 'if' '(' expression ')' '{' statements '}' ('else' '{' 
                   statements '}')?
    - whileStatement: 'while' '(' 'expression' ')' '{' statements '}'
    - doStatement: 'do' subroutineCall ';'
    - returnStatement: 'return' expression? ';'

    ## Expressions
    
    - expression: term (op term)*
    - term: integerConstant | stringConstant | keywordConstant | varName | 
            varName '['expression']' | subroutineCall | '(' expression ')' | 
            unaryOp term
    - subroutineCall: subroutineName '(' expressionList ')' | (className | 
                      varName) '.' subroutineName '(' expressionList ')'
    - expressionList: (expression (',' expression)* )?
    - op: '+' | '-' | '*' | '/' | '&' | '|' | '<' | '>' | '='
    - unaryOp: '-' | '~' | '^' | '#'
    - keywordConstant: 'true' | 'false' | 'null' | 'this'
    
    Note that ^, # correspond to shiftleft and shiftright, respectively.
    """

    def __init__(self, input_stream: typing.TextIO) -> None:
        """Opens the input stream and gets ready to tokenize it.

        Args:
            input_stream (typing.TextIO): input stream.
        """
        # Read the entire input and remove comments
        content = input_stream.read()
        self._tokens = self._tokenize(self._remove_comments(content))
        self._current_token = None
        self._current_index = -1

    def _remove_comments(self, content: str) -> str:
        """Removes all types of comments from the input content."""
        # Remove /* ... */ comments
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        # Remove /** ... */ comments
        content = re.sub(r'/\*\*.*?\*/', '', content, flags=re.DOTALL)
        # Remove // comments
        content = re.sub(r'//.*?$', '', content, flags=re.MULTILINE)
        return content

    def _tokenize(self, content: str) -> list:
        """Breaks the content into tokens."""
        tokens = []
        # Regular expressions for different token types
        patterns = [
            (r'"[^"]*"', STRING_CONST),  # String constants
            (r'\d+', INT_CONST),         # Integer constants
            (r'[a-zA-Z_][a-zA-Z0-9_]*', IDENTIFIER),  # Identifiers
            (r'[{}()[\].,;+\-*/&|<>=~^#]', SYMBOL)    # Symbols
        ]
        
        # Combine all patterns
        pattern = '|'.join(f'({p})' for p, _ in patterns)
        
        # Find all matches
        for match in re.finditer(pattern, content):
            token = match.group()
            # Skip whitespace
            if token.isspace():
                continue
                
            # Determine token type
            token_type = None
            for _, t_type in patterns:
                if re.match(f'^{patterns[patterns.index((_, t_type))][0]}$', token):
                    token_type = t_type
                    break
            
            # Handle keywords
            if token_type == IDENTIFIER and token.lower() in KEYWORDS:
                token_type = KEYWORD
                
            tokens.append((token, token_type))
            
        return tokens

    def has_more_tokens(self) -> bool:
        """Do we have more tokens in the input?

        Returns:
            bool: True if there are more tokens, False otherwise.
        """
        return self._current_index < len(self._tokens) - 1

    def advance(self) -> None:
        """Gets the next token from the input and makes it the current token. 
        This method should be called if has_more_tokens() is true. 
        Initially there is no current token.
        """
        if self.has_more_tokens():
            self._current_token = self._tokens[self._current_index + 1]
            self._current_index += 1

    def token_type(self) -> str:
        """
        Returns:
            str: the type of the current token, can be
            "KEYWORD", "SYMBOL", "IDENTIFIER", "INT_CONST", "STRING_CONST"
        """
        return self._current_token[1]

    def keyword(self) -> str:
        """
        Returns:
            str: the keyword which is the current token.
            Should be called only when token_type() is "KEYWORD".
            Can return "CLASS", "METHOD", "FUNCTION", "CONSTRUCTOR", "INT", 
            "BOOLEAN", "CHAR", "VOID", "VAR", "STATIC", "FIELD", "LET", "DO", 
            "IF", "ELSE", "WHILE", "RETURN", "TRUE", "FALSE", "NULL", "THIS"
        """
        return self._current_token[0]

    def symbol(self) -> str:
        """
        Returns:
            str: the character which is the current token.
            Should be called only when token_type() is "SYMBOL".
            Recall that symbol was defined in the grammar like so:
            symbol: '{' | '}' | '(' | ')' | '[' | ']' | '.' | ',' | ';' | '+' | 
              '-' | '*' | '/' | '&' | '|' | '<' | '>' | '=' | '~' | '^' | '#'
        """
        return self._current_token[0]

    def identifier(self) -> str:
        """
        Returns:
            str: the identifier which is the current token.
            Should be called only when token_type() is "IDENTIFIER".
            Recall that identifiers were defined in the grammar like so:
            identifier: A sequence of letters, digits, and underscore ('_') not 
                  starting with a digit. You can assume keywords cannot be
                  identifiers, so 'self' cannot be an identifier, etc'.
        """
        return self._current_token[0]

    def int_val(self) -> int:
        """
        Returns:
            str: the integer value of the current token.
            Should be called only when token_type() is "INT_CONST".
            Recall that integerConstant was defined in the grammar like so:
            integerConstant: A decimal number in the range 0-32767.
        """
        return int(self._current_token[0])

    def string_val(self) -> str:
        """
        Returns:
            str: the string value of the current token, without the double 
            quotes. Should be called only when token_type() is "STRING_CONST".
            Recall that StringConstant was defined in the grammar like so:
            StringConstant: '"' A sequence of Unicode characters not including 
                      double quote or newline '"'
        """
        # Remove the surrounding double quotes
        return self._current_token[0][1:-1]

    def get_token_representation(self) -> str:
        """Get a string representation of the current token."""
        token_type = self.token_type()
        if token_type == KEYWORD:
            return f"<keyword> {self.keyword()} </keyword>"
        elif token_type == SYMBOL:
            symbol = self.symbol()
            # Handle special XML characters
            if symbol == "<":
                symbol = "&lt;"
            elif symbol == ">":
                symbol = "&gt;"
            elif symbol == "&":
                symbol = "&amp;"
            # Handle unary operators
            elif symbol == "^":
                symbol = "^"
            elif symbol == "#":
                symbol = "#"
            return f"<symbol> {symbol} </symbol>"
        elif token_type == IDENTIFIER:
            return f"<identifier> {self.identifier()} </identifier>"
        elif token_type == INT_CONST:
            return f"<integerConstant> {self.int_val()} </integerConstant>"
        elif token_type == STRING_CONST:
            return f"<stringConstant> {self.string_val()} </stringConstant>"
        return ""
