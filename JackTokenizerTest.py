import sys
import os
from JackTokenizer import JackTokenizer
from typing import List, Tuple
from difflib import unified_diff
import xml.etree.ElementTree as ET

def read_expected_tokens(file_path: str) -> List[str]:
    """Read the expected tokens from the comparison file."""
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def get_token_representation(tokenizer: JackTokenizer) -> str:
    """Get a string representation of the current token."""
    token_type = tokenizer.token_type()
    if token_type == "KEYWORD":
        return f"<keyword> {tokenizer.keyword()} </keyword>"
    elif token_type == "SYMBOL":
        symbol = tokenizer.symbol()
        # Handle special XML characters
        if symbol == "<":
            symbol = "&lt;"
        elif symbol == ">":
            symbol = "&gt;"
        elif symbol == "&":
            symbol = "&amp;"
        return f"<symbol> {symbol} </symbol>"
    elif token_type == "IDENTIFIER":
        return f"<identifier> {tokenizer.identifier()} </identifier>"
    elif token_type == "INT_CONST":
        return f"<integerConstant> {tokenizer.int_val()} </integerConstant>"
    elif token_type == "STRING_CONST":
        return f"<stringConstant> {tokenizer.string_val()} </stringConstant>"
    return ""

def tokenize_file(input_file: str) -> List[str]:
    """Tokenize the input file and return list of token representations."""
    tokens = []
    with open(input_file, 'r') as f:
        tokenizer = JackTokenizer(f)
        while tokenizer.has_more_tokens():
            tokenizer.advance()
            tokens.append(get_token_representation(tokenizer))
    return tokens

def compare_tokens(actual: List[str], expected: List[str]) -> Tuple[bool, List[str]]:
    """Compare actual and expected tokens and return differences."""
    # Normalize both lists by removing empty lines and stripping whitespace
    actual = [line.strip() for line in actual if line.strip()]
    expected = [line.strip() for line in expected if line.strip()]
    
    differences = list(unified_diff(
        expected, actual,
        fromfile='expected', tofile='actual',
        lineterm=''
    ))
    return len(differences) == 0, differences

def main():
    if len(sys.argv) != 3:
        print("Usage: python JackTokenizerTest.py <input_file> <compare_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    compare_file = sys.argv[2]

    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        sys.exit(1)
    if not os.path.exists(compare_file):
        print(f"Error: Compare file '{compare_file}' does not exist.")
        sys.exit(1)

    print(f"\nTokenizing file: {input_file}")
    print(f"Comparing with: {compare_file}\n")

    # Get actual tokens
    actual_tokens = tokenize_file(input_file)
    
    # Wrap with <tokens> ... </tokens>
    actual_tokens = ["<tokens>"] + [f"  {line}" for line in actual_tokens] + ["</tokens>"]
    
    # Write actual output to TestOutput.xml
    with open("TestOutput.xml", "w") as f:
        f.write("\n".join(actual_tokens))
    
    # Get expected tokens
    expected_tokens = read_expected_tokens(compare_file)

    # Compare and show results
    is_match, differences = compare_tokens(actual_tokens, expected_tokens)

    if is_match:
        print("✅ Tokenization matches expected output!")
    else:
        print("❌ Tokenization differs from expected output:")
        print("\nDifferences:")
        for diff in differences:
            if diff.startswith('+'):
                print(f"\033[92m{diff}\033[0m")  # Green for additions
            elif diff.startswith('-'):
                print(f"\033[91m{diff}\033[0m")  # Red for deletions
            elif diff.startswith('@'):
                print(f"\033[94m{diff}\033[0m")  # Blue for headers

        print("\nToken counts:")
        print(f"Expected tokens: {len(expected_tokens)}")
        print(f"Actual tokens: {len(actual_tokens)}")

if __name__ == "__main__":
    main() 