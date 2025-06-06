"""
This file is part of nand2tetris, as taught in The Hebrew University, and
was written by Aviv Yaish. It is an extension to the specifications given
[here](https://www.nand2tetris.org) (Shimon Schocken and Noam Nisan, 2017),
as allowed by the Creative Common Attribution-NonCommercial-ShareAlike 3.0
Unported [License](https://creativecommons.org/licenses/by-nc-sa/3.0/).
"""

import os
import sys
from typing import List
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine


class JackAnalyzer:
    """Top-down compiler for the Jack language.
    
    The JackAnalyzer is the main class that orchestrates the compilation process.
    It takes Jack source files as input and produces XML files that represent
    the syntactic structure of the Jack programs.
    
    The compilation process consists of two main stages:
    1. Tokenization: Breaking the source code into tokens
    2. Parsing: Analyzing the tokens and generating XML output
    
    The JackAnalyzer can process either a single Jack file or a directory
    containing multiple Jack files.
    """

    def __init__(self, input_path: str) -> None:
        """Initializes the Jack analyzer with the input path.

        Args:
            input_path (str): Path to a Jack file or directory containing Jack files
        """
        self.input_path = input_path
        self.jack_files: List[str] = []

    def _get_jack_files(self) -> None:
        """Gets all Jack files from the input path."""
        if os.path.isfile(self.input_path):
            if self.input_path.endswith('.jack'):
                self.jack_files = [self.input_path]
        elif os.path.isdir(self.input_path):
            self.jack_files = [
                os.path.join(self.input_path, f)
                for f in os.listdir(self.input_path)
                if f.endswith('.jack')
            ]
        else:
            raise ValueError(f"Invalid input path: {self.input_path}")

    def analyze(self) -> None:
        """Analyzes all Jack files and generates corresponding XML files."""
        self._get_jack_files()
        
        for jack_file in self.jack_files:
            xml_file = jack_file.replace('.jack', 'Test.xml')
            
            try:
                with open(jack_file, 'r') as input_file, open(xml_file, 'w') as output_file:
                    # Create the compilation engine
                    engine = CompilationEngine(input_file, output_file)
                    
                    # Compile the class
                    engine.compile_class()
                    
                print(f"Successfully compiled {jack_file} to {xml_file}")
            except Exception as e:
                print(f"Error processing {jack_file}: {str(e)}")


def main():
    """Main function to run the Jack analyzer."""
    if len(sys.argv) != 2:
        print("Usage: python JackAnalyzer.py <input_path>")
        print("  <input_path>: Path to a Jack file or directory containing Jack files")
        sys.exit(1)
    
    try:
        analyzer = JackAnalyzer(sys.argv[1])
        analyzer.analyze()
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
