#!/bin/bash

# Specify the directory containing the files
directory="../dataset"

for dir in "$directory"/*; do
    if [ -d "$dir" ]; then
        for file in "$dir"/*; do
            if [ -f "$file" ] && [[ "$file" == *.sol ]]; then
                # Extract pragma versions from the file
                pragma_version=$(grep -oP '^[\s\t]*pragma\s+solidity\s+([^\s\t;]+)' "$file" | sed -E 's/^\s*pragma\s+solidity\s+//')
                if [ -n "$pragma_version" ]; then
                    echo "$file $pragma_version"
                fi
            fi
        done

    fi
done