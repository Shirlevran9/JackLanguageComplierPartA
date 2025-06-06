"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

import typing
from JackTokenizer import JackTokenizer


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
        
        # class variable declarations
        self.tokenizer.advance()
        while self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword() in ["static", "field"]:
            self.compile_class_var_dec()
            self.tokenizer.advance()  # Advance after the semicolon
        
        # subroutine declarations
        while self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword() in ["constructor", "function", "method"]:
            self.compile_subroutine()
            self.tokenizer.advance()  # Advance after the closing brace
        
        # Write the closing brace
        self._write_token()
        
        self._write_non_terminal_end("class")

    def compile_class_var_dec(self) -> None:
        """Compiles a static or field declaration."""
        self._write_non_terminal_start("classVarDec")
        
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
        
        self._write_non_terminal_end("classVarDec")

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
        self.tokenizer.advance()
        self.compile_parameter_list()
        
        # Write the subroutine body
        self.compile_subroutine_body()
        
        self._write_non_terminal_end("subroutineDec")

    def compile_parameter_list(self) -> None:
        """Compiles a (possibly empty) parameter list."""
        self._write_non_terminal_start("parameterList")
        
        # Write the opening parenthesis
        self._write_token()
        
        # Write parameters if any
        self.tokenizer.advance()
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != ")":
            while True:
                # Write the type
                self._write_token()
                
                # Write the parameter name
                self.tokenizer.advance()
                self._write_token()
                
                # Check for more parameters
                self.tokenizer.advance()
                if self.tokenizer.token_type() == "SYMBOL":
                    if self.tokenizer.symbol() == ")":
                        break
                    elif self.tokenizer.symbol() == ",":
                        self._write_token()
                        self.tokenizer.advance()
        
        # Write the closing parenthesis
        self._write_token()
        
        self._write_non_terminal_end("parameterList")

    def compile_subroutine_body(self) -> None:
        """Compiles a subroutine's body."""
        self._write_non_terminal_start("subroutineBody")
        
        # Write the opening brace
        self.tokenizer.advance()
        self._write_token()
        
        # Write variable declarations
        while self.tokenizer.has_more_tokens():
            self.tokenizer.advance()
            if self.tokenizer.token_type() == "KEYWORD" and self.tokenizer.keyword() == "var":
                self.compile_var_dec()
            else:
                break
        
        # Write statements
        self.compile_statements()
        
        # Write the closing brace
        self._write_token()
        
        self._write_non_terminal_end("subroutineBody")

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
        self._write_non_terminal_start("statements")
        
        while self.tokenizer.token_type() == "KEYWORD":
            keyword = self.tokenizer.keyword()
            if keyword == "let":
                self.compile_let()
            elif keyword == "if":
                self.compile_if()
            elif keyword == "while":
                self.compile_while()
            elif keyword == "do":
                self.compile_do()
            elif keyword == "return":
                self.compile_return()
            else:
                break
        
        self._write_non_terminal_end("statements")

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
        self._write_non_terminal_start("doStatement")
        
        # Write the do keyword
        self._write_token()
        
        # Write the subroutine call
        self.tokenizer.advance()
        self.compile_subroutine_call()
        
        # Write the semicolon
        self._write_token()
        
        self.tokenizer.advance()
        self._write_non_terminal_end("doStatement")

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
        # Write the opening parenthesis or dot
        self._write_token()
        
        # If it's a method call, write the method name
        if self.tokenizer.symbol() == ".":
            self.tokenizer.advance()
            self._write_token()
        
        # Write the opening parenthesis
        self.tokenizer.advance()
        self._write_token()
        
        # Write the expression list
        self.tokenizer.advance()
        self.compile_expression_list()
        
        # Write the closing parenthesis
        self._write_token()
        
        self.tokenizer.advance()

    def compile_expression_list(self) -> None:
        """Compiles a (possibly empty) comma-separated list of expressions."""
        self._write_non_terminal_start("expressionList")
        
        if self.tokenizer.token_type() != "SYMBOL" or self.tokenizer.symbol() != ")":
            while True:
                self.compile_expression()
                if self.tokenizer.token_type() == "SYMBOL":
                    if self.tokenizer.symbol() == ")":
                        break
                    elif self.tokenizer.symbol() == ",":
                        self._write_token()
                        self.tokenizer.advance()
        
        self._write_non_terminal_end("expressionList")
