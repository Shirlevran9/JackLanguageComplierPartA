#!/bin/bash

# Check if a directory is provided
if [ $# -ne 1 ]; then
    echo "Usage: $0 <directory>"
    exit 1
fi

DIR="$1"

# Check if directory exists
if [ ! -d "$DIR" ]; then
    echo "Error: Directory '$DIR' does not exist"
    exit 1
fi

# Compile the directory using our compiler
echo "Compiling $DIR..."
python JackAnalyzer.py "$DIR"

# Find all .xml files in the directory
XML_FILES=("$DIR"/*.xml)

if [ ${#XML_FILES[@]} -eq 0 ]; then
    echo "No .xml files found in $DIR."
    exit 1
fi

# Compare each .xml file with its reference version in ../../projectsRef/10/
ALL_MATCHED=true
for file in "${XML_FILES[@]}"; do
    base="$(basename "$file" .xml)"
    ref_file="../../projectsRef/10/$DIR/${base}T.xml"
    if [ -f "$ref_file" ]; then
        echo "Comparing $file with $ref_file..."
        # Compare files ignoring whitespace differences
        diff -u -w "$file" "$ref_file"
        if [ $? -ne 0 ]; then
            ALL_MATCHED=false
        fi
    else
        echo "Reference file $ref_file not found. Skipping."
    fi
done

if $ALL_MATCHED; then
    echo -e "\nSuccess! All outputs match their references."
else
    echo -e "\nDifferences found between outputs and references."
fi 