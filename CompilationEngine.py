"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

import typing
from JackTokenizer import JackTokenizer
from Constants import *


class CompilationEngine:
    """Generates XML output according to the Jack grammar rules.
    
    The CompilationEngine takes a JackTokenizer as input and generates a structured
    XML output that represents the syntactic structure of the Jack program.
    
    The compilation process follows the Jack grammar rules defined in the JackTokenizer
    documentation, including:
    - Class declarations
    - Class variable declarations
    - Subroutine declarations
    - Parameter lists
    - Variable declarations
    - Statements
    - Expressions
    """

    def __init__(self, input_stream: typing.TextIO, output_stream: typing.TextIO) -> None:
        """Initializes the compilation engine with input and output streams.

        Args:
            input_stream (typing.TextIO): The input stream containing Jack code
            output_stream (typing.TextIO): The output stream for XML output
        """
        self.tokenizer = JackTokenizer(input_stream)
        self.output = output_stream
        self.indent_level = 0
        self.indent = "  "  # Two spaces for indentation

    def _write_token(self) -> None:
        """Writes the current token to the output stream with proper indentation."""
        token_representation = self.tokenizer.get_token_representation()
        self.output.write(f"{self.indent * self.indent_level}{token_representation}\n")

    def _write_non_terminal_start(self, non_terminal: str) -> None:
        """Writes the start tag of a non-terminal element.

        Args:
            non_terminal (str): The name of the non-terminal element
        """
        self.output.write(f"{self.indent * self.indent_level}<{non_terminal}>\n")
        self.indent_level += 1

    def _write_non_terminal_end(self, non_terminal: str) -> None:
        """Writes the end tag of a non-terminal element.

        Args:
            non_terminal (str): The name of the non-terminal element
        """
        self.indent_level -= 1
        self.output.write(f"{self.indent * self.indent_level}</{non_terminal}>\n")

    def compile_class(self) -> None:
        """Compiles a complete class."""
        
        self._write_class_begining()
        
        # class variable declarations
        self.tokenizer.advance()
        while self._is_class_var_dec():
            self.compile_class_var_dec()
            self.tokenizer.advance()  # Advance after the semicolon
        
        # subroutine declarations
        while self._is_subroutine_dec():
            self.compile_subroutine()
            self.tokenizer.advance()  # Advance after the closing brace
        
        # Write the closing brace
        self._write_token()
        
        self._write_non_terminal_end("class")
    
    def _write_class_begining(self) -> None:
        """Writes the beginning of a class."""
        self._write_non_terminal_start("class")
        
        # 'class' keyword
        self.tokenizer.advance()
        self._write_token()
        
        # class name
        self.tokenizer.advance()
        self._write_token()
        
        # '{'
        self.tokenizer.advance()
        self._write_token()
        return

    # All _is_x functions are used to check if the current token is a certain type of declaration
    def _is_class_var_dec(self) -> bool:
        """Checks if the current token is a class variable declaration."""
        return self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword() in ["static", "field"]
    
    def _is_subroutine_dec(self) -> bool:
        """Checks if the current token is a subroutine declaration."""
        return self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword() in ["constructor", "function", "method"]
    
    def _is_parameter_list(self) -> bool:
        """Checks if the current token is a parameter list."""
        if self.tokenizer.token_type() == "SYMBOL":
            return self.tokenizer.symbol() != ")"
        elif self.tokenizer.token_type() in ["KEYWORD", "IDENTIFIER"]:
            return True
        return False
    
    def _is_var_dec(self) -> bool:
        """Checks if the current token is a variable declaration."""
        return self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword() == "var"
    
    def _is_let_dec(self) -> bool:
        """Checks if the current token is a let declaration."""
        return self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword() == "let"
    
    def _is_if_dec(self) -> bool:
        """Checks if the current token is an if declaration."""
        return self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword() == "if"
    
    def _is_while_dec(self) -> bool:
        """Checks if the current token is a while declaration."""
        return self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword() == "while"
    
    def _is_subroutine_dec_part(self) -> bool:
        """Checks if the current token is a valid part of a subroutine declaration."""
        return self.tokenizer.symbol() != "}"
        
    def _is_statements_dec_part(self) -> bool:
        """Checks if the current token is a valid part of a statements declaration."""
        return self.tokenizer.token_type() == KEYWORD and self.tokenizer.keyword() in [LET, IF, WHILE, DO, RETURN]
    
    def compile_class_var_dec(self) -> None:
        """Compiles a static or field declaration."""
        self._write_non_terminal_start(CLASS_VAR_DEC)
        
        # Write the static/field keyword
        self._write_token()
        
        # Write the type
        self.tokenizer.advance()
        self._write_token()
        
        # Write the variable name
        self.tokenizer.advance()
        self._write_token()
        
        # Write additional variable names if any
        while True:
            self.tokenizer.advance()
            if self.tokenizer.token_type() == "SYMBOL":
                if self.tokenizer.symbol() == ";":
                    self._write_token()
                    break
                elif self.tokenizer.symbol() == ",":
                    self._write_token()
                    self.tokenizer.advance()
                    self._write_token()
        
        self._write_non_terminal_end(CLASS_VAR_DEC)

    def compile_subroutine(self) -> None:
        """Compiles a complete subroutine."""
        self._write_non_terminal_start("subroutineDec")
        
        # Write the subroutine type (constructor/function/method)
        self._write_token()
        
        # Write the return type
        self.tokenizer.advance()
        self._write_token()
        
        # Write the subroutine name
        self.tokenizer.advance()
        self._write_token()
        
        # Write the parameter list
        self.compile_parameter_list()
        
        # Write the subroutine body
        self.compile_subroutine_body()
        
        self._write_non_terminal_end("subroutineDec")

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list. 
        Starts after the opening parenthesis (
        """
        # Write open parenthesis (
        self.tokenizer.advance()
        self._write_token()
        
        # Write the parameter list
        self._write_non_terminal_start(PARAMETER_LIST_DEC)
        
        # Write parameters if any
        self.tokenizer.advance()
        while self._is_parameter_list():
            # Write the type
            self._write_token()
            
            # Write the parameter name
            self.tokenizer.advance()
            self._write_token()
            
            # Check for more parameters
            self.tokenizer.advance()
        
        self._write_non_terminal_end(PARAMETER_LIST_DEC)
        # Write the closing parenthesis
        self._write_token()

    def compile_subroutine_body(self) -> None:
        """Compiles a subroutine's body."""
        self._write_non_terminal_start(SUBROUTINE_BODY_DEC)
        
        # Write the opening brace {
        self.tokenizer.advance()
        self._write_token()
        
        # Write variable declarations
        self.tokenizer.advance()
        while self._is_var_dec():
            self.compile_var_dec()
            self.tokenizer.advance()
        
        # Write statements
        self.compile_statements()
        
        # Write the closing brace }
        self._write_token()
        
        self._write_non_terminal_end(SUBROUTINE_BODY_DEC)

    def compile_var_dec(self) -> None:
        """Compiles a var declaration."""
        self._write_non_terminal_start("varDec")
        
        # Write the var keyword
        self._write_token()
        
        # Write the type
        self.tokenizer.advance()
        self._write_token()
        
        # Write the variable name
        self.tokenizer.advance()
        self._write_token()
        
        # Write additional variable names if any
        while self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
            if self.tokenizer.token_type() == "SYMBOL":
                if self.tokenizer.symbol() == ";":
                    self._write_token()
                    break
                elif self.tokenizer.symbol() == ",":
                    self._write_token()
                    self.tokenizer.advance()
                    self._write_token()
        
        self._write_non_terminal_end("varDec")

    def compile_statements(self) -> None:
        """Compiles a sequence of statements."""
        self._write_non_terminal_start(STATEMENTS_DEC)
        
        while self._is_statements_dec_part():
            keyword = self.tokenizer.keyword()
            if keyword == LET:
                self.compile_let()
            elif keyword == IF:
                self.compile_if()
            elif keyword == WHILE:
                self.compile_while()
            elif keyword == DO:
                self.compile_do()
            elif keyword == RETURN:
                self.compile_return()
            else:
                break
        
        self._write_non_terminal_end(STATEMENTS_DEC)

    def compile_let(self) -> None:
        """Compiles a let statement."""
        self._write_non_terminal_start("letStatement")
        
        # Write the let keyword
        self._write_token()
        
        # Write the variable name
        self.tokenizer.advance()
        self._write_token()
        
        # Check for array access
        self.tokenizer.advance()
        if self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == "[":
            self._write_token()  # [
            self.tokenizer.advance()
            self.compile_expression()
            self._write_token()  # ]
            self.tokenizer.advance()
        
        # Write the equals sign
        self._write_token()
        
        # Write the expression
        self.tokenizer.advance()
        self.compile_expression()
        
        # Write the semicolon
        self._write_token()
        
        self.tokenizer.advance()
        self._write_non_terminal_end("letStatement")

    def compile_if(self) -> None:
        """Compiles an if statement."""
        self._write_non_terminal_start("ifStatement")
        
        # Write the if keyword
        self._write_token()
        
        # Write the condition
        self.tokenizer.advance()
        self._write_token()  # Opening parenthesis
        self.tokenizer.advance()
        self.compile_expression()
        self._write_token()  # Closing parenthesis
        
        # Write the then block
        self.tokenizer.advance()
        self._write_token()  # Opening brace
        self.tokenizer.advance()
        self.compile_statements()
        self._write_token()  # Closing brace
        
        # Check for else block
        self.tokenizer.advance()
        if self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword() == "else":
            self._write_token()
            self.tokenizer.advance()
            self._write_token()  # Opening brace
            self.tokenizer.advance()
            self.compile_statements()
            self._write_token()  # Closing brace
            self.tokenizer.advance()
        
        self._write_non_terminal_end("ifStatement")

    def compile_while(self) -> None:
        """Compiles a while statement."""
        self._write_non_terminal_start("whileStatement")
        
        # Write the while keyword
        self._write_token()
        
        # Write the condition
        self.tokenizer.advance()
        self._write_token()  # Opening parenthesis
        self.tokenizer.advance()
        self.compile_expression()
        self._write_token()  # Closing parenthesis
        
        # Write the body
        self.tokenizer.advance()
        self._write_token()  # Opening brace
        self.tokenizer.advance()
        self.compile_statements()
        self._write_token()  # Closing brace
        
        self.tokenizer.advance()
        self._write_non_terminal_end("whileStatement")

    def compile_do(self) -> None:
        """Compiles a do statement."""
        self._write_non_terminal_start(DO_STATEMENT_DEC)
        
        # Write the do keyword
        self._write_token()
        
        # Write the subroutine call
        self.tokenizer.advance()
        self.compile_subroutine_call()
        
        # Write the semicolon
        self._write_token()
        
        self.tokenizer.advance()
        self._write_non_terminal_end(DO_STATEMENT_DEC)

    def compile_return(self) -> None:
        """Compiles a return statement."""
        self._write_non_terminal_start("returnStatement")
        
        # Write the return keyword
        self._write_token()
        
        # Check for return value
        self.tokenizer.advance()
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != ";":
            self.compile_expression()
        
        # Write the semicolon
        self._write_token()
        
        self.tokenizer.advance()
        self._write_non_terminal_end("returnStatement")

    def compile_expression(self) -> None:
        """Compiles an expression."""
        self._write_non_terminal_start("expression")
        
        # Write the first term
        self.compile_term()
        
        # Write additional terms if any
        while self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() in ["+", "-", "*", "/", "&", "|", "<", ">", "="]:
            self._write_token()  # Write the operator
            self.tokenizer.advance()
            self.compile_term()
        
        self._write_non_terminal_end("expression")

    def compile_term(self) -> None:
        """Compiles a term."""
        self._write_non_terminal_start("term")
        
        if self.tokenizer.token_type() == "INT_CONST":
            self._write_token()
            self.tokenizer.advance()
        elif self.tokenizer.token_type() == "STRING_CONST":
            self._write_token()
            self.tokenizer.advance()
        elif self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword() in ["true", "false", "null", "this"]:
            self._write_token()
            self.tokenizer.advance()
        elif self.tokenizer.token_type() == "IDENTIFIER":
            self._write_token()
            self.tokenizer.advance()
            
            if self.tokenizer.token_type() == "SYMBOL":
                if self.tokenizer.symbol() == "[":
                    self._write_token()
                    self.tokenizer.advance()
                    self.compile_expression()
                    self._write_token()  # Closing bracket
                    self.tokenizer.advance()
                elif self.tokenizer.symbol() in ["(", "."]:
                    self.compile_subroutine_call()
        elif self.tokenizer.token_type() == "SYMBOL":
            if self.tokenizer.symbol() == "(":
                self._write_token()
                self.tokenizer.advance()
                self.compile_expression()
                self._write_token()  # Closing parenthesis
                self.tokenizer.advance()
            elif self.tokenizer.symbol() in ["-", "~", "^", "#"]:
                self._write_token()
                self.tokenizer.advance()
                self.compile_term()
        
        self._write_non_terminal_end("term")

    def compile_subroutine_call(self) -> None:
        """Compiles a subroutine call."""
               
        # Write var, . or method name
        while (self.tokenizer.token_type() == IDENTIFIER and self.tokenizer.symbol() != "(") or (self.tokenizer.token_type() == SYMBOL and self.tokenizer.symbol() == ".") :
            self._write_token()
            self.tokenizer.advance()
        
        # Reached the opening parenthesis - write "("
        self._write_token()
        
        # Write the expression list
        self.compile_expression_list()
        
        # Write the closing parenthesis
        self._write_token()
        
        self.tokenizer.advance()

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        self._write_non_terminal_start(EXPRESION_LIST_DEC)
        self.tokenizer.advance()
        
        # Check if there are any expressions (not a closing parenthesis)
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != ")":
            # Compile the first expression
            self.compile_expression()
            
            # Compile additional expressions separated by commas
            while self.tokenizer.token_type() == "SYMBOL" and self.tokenizer.symbol() == ",":
                self._write_token()  # Write the comma
                self.tokenizer.advance()
                self.compile_expression()
        
        self._write_non_terminal_end(EXPRESION_LIST_DEC)
