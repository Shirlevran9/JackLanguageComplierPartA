#!/bin/bash

# Script to zip project files for submission
# Creates project10.zip with all necessary files

echo "Creating project10.zip with project files..."

# Remove existing zip file if it exists
if [ -f "project10.zip" ]; then
    echo "Removing existing project10.zip..."
    rm project10.zip
fi

# List of files to include in the zip
FILES=(
    "Constants.py"
    "JackAnalyzer.py"
    "CompilationEngine.py"
    "JackTokenizer.py"
    "JackAnalyzer"
    "Makefile"
    "AUTHORS"
)

# Check if all files exist before zipping
missing_files=()
for file in "${FILES[@]}"; do
    if [ ! -f "$file" ]; then
        missing_files+=("$file")
    fi
done

# Report missing files
if [ ${#missing_files[@]} -gt 0 ]; then
    echo "Warning: The following files are missing:"
    for file in "${missing_files[@]}"; do
        echo "  - $file"
    done
    echo ""
fi

# Create the zip file with existing files
existing_files=()
for file in "${FILES[@]}"; do
    if [ -f "$file" ]; then
        existing_files+=("$file")
    fi
done

if [ ${#existing_files[@]} -gt 0 ]; then
    echo "Zipping the following files:"
    for file in "${existing_files[@]}"; do
        echo "  - $file"
    done
    
    zip project10.zip "${existing_files[@]}"
    
    if [ $? -eq 0 ]; then
        echo ""
        echo "✅ Successfully created project10.zip"
        echo "📁 Contents:"
        unzip -l project10.zip
    else
        echo "❌ Error creating project10.zip"
        exit 1
    fi
else
    echo "❌ No files found to zip!"
    exit 1
fi 