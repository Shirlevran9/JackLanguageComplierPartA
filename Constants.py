""" 
This file contains all constants used in the project.
"""

KEYWORDS = ["class", "constructor", "function", "method", "field", "static", "var", "int", "char", "boolean", "void", "true", "false", "null", "this", "let", "do", "if", "else", "while", "return"]
SYMBOLS = ["{", "}", "(", ")", "[", "]", ".", ",", ";", "+", "-", "*", "/", "&", "|", "<", ">", "=", "~"]
OPERATORS = ["+", "-", "*", "/", "&", "|", "<", ">", "=", "~"]
UNARY_OPERATORS = ["-", "~"]

# Types
INT_TYPE = "int"
CHAR_TYPE = "char"
BOOLEAN_TYPE = "boolean"
VOID_TYPE = "void"

# Subroutine types
CONSTRUCTOR_TYPE = "constructor"
FUNCTION_TYPE = "function"
METHOD_TYPE = "method"

KEYWORD = "KEYWORD"
SYMBOL = "SYMBOL"
IDENTIFIER = "IDENTIFIER"
INT_CONST = "INT_CONST"
STRING_CONST = "STRING_CONST"


# XML tags for non-terminal elements
PARAMETER_LIST_DEC = "parameterList"
SUBROUTINE_BODY_DEC = "subroutineBody"
STATEMENTS_DEC = "statements"
EXPRESION_DEC = "expression"
EXPRESION_LIST_DEC = "expressionList"
CLASS_VAR_DEC = "classVarDec"
DO_STATEMENT_DEC = "doStatement"

# Keywords
LET = "let"
IF = "if"
WHILE = "while"
DO = "do"
RETURN = "return"
TRUE = "true"
FALSE = "false"
NULL = "null"
THIS = "this"
VAR = "var"