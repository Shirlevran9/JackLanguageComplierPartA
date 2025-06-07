"""
This file is a test to compare 2 xml files
The program will show every row - the difference between the target and the actual file if exists
O.W will print that we succeeded
"""

import sys
import os

def compare_files(file1_path, file2_path):
    """Compare two files line by line and show differences."""
    try:
        with open(file1_path, 'r') as file1, open(file2_path, 'r') as file2:
            lines1 = file1.readlines()
            lines2 = file2.readlines()
        
        max_lines = max(len(lines1), len(lines2))
        differences_found = False
        
        print(f"Comparing {file1_path} (actual) vs {file2_path} (expected)")
        print("=" * 80)
        
        for i in range(max_lines):
            if i > min(len(lines1), len(lines2)):
                print("Finished comparing files, lines are equal")
                return
            line1 = lines1[i].rstrip() if i < len(lines1) else "<EOF>"
            line2 = lines2[i].rstrip() if i < len(lines2) else "<EOF>"
            
            if line1 != line2:
                differences_found = True
                print(f"Line {i + 1}:")
                print(f"  Actual  : '{line1}'")
                print(f"  Expected: '{line2}'")
                print()
        
        if not differences_found:
            print("SUCCESS! Files are identical.")
        else:
            print(f"FAILED! Found {sum(1 for i in range(max_lines) if (lines1[i].rstrip() if i < len(lines1) else '<EOF>') != (lines2[i].rstrip() if i < len(lines2) else '<EOF>'))} differences.")
            
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
    except Exception as e:
        print(f"Error: {e}")


def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) < 2:
        print("Usage: python TestTwoDiff.py <actual_file> (<expected_file>)?")
        print("  <actual_file>: Path to the actual output file")
        print("  <expected_file>: Path to the expected output file")
        sys.exit(1)
    
    
    actual_file = sys.argv[1]
    if len(sys.argv) == 3:
        expected_file = sys.argv[2]
    elif os.path.isdir(actual_file): # If it is a directory - process all files in the directory
        for file in os.listdir(actual_file):
            if file.endswith(".xml") and not file.endswith("Test.xml") and not file.endswith("T.xml"):
                print(f"Comparing {file} (actual) vs {file.replace('.xml', 'Test.xml')} (expected)")
                compare_files(os.path.join(actual_file, file), os.path.join(actual_file, file.replace(".xml", "Test.xml")))
        print("Finished comparing files, all files are identical")
        return
    else:
        expected_file = actual_file.replace(".xml", "Test.xml")
        print(f"No expected file provided, using {expected_file} as expected file")
    
    compare_files(actual_file, expected_file)


if __name__ == "__main__":
    main()
