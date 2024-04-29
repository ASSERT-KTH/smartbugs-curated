#!/bin/bash

if [ $# -eq 0 ]; then
    echo "Error: CSV file path not provided."
    exit 1
fi

process_csv() {
    local path="$1"
    local pragma_version="$2"
    echo "Path: $path, Pragma Version: $pragma_version"

    solc-select use "$pragma_version" --always-install
    output=$(solc --ast-json "../$path")
    
    json=$(echo "$output" | tail -n +5 | head -n -1)
    
    echo "$json" > "../${path%.sol}.ast"
}

while IFS=' ' read -r path pragma_version; do
    process_csv "$path" "$pragma_version"
done < "$1"