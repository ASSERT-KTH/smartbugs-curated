#!/bin/bash

if [ $# -ne 2 ]; then
    echo "Usage: $0 <csv_path> <output_dir>"
    exit 1
fi

CSV=$1
output=$2

process_csv() {
    local path="../$1"
    local pragma_version="$2"
    echo "Path: $path, Pragma Version: $pragma_version"

    solc-select use "$pragma_version" --always-install
	filename=$(basename -- "$path")
	inputdir=$(dirname "$path")
	basedir=$(basename -- "$inputdir")
	outputdir=$output$basedir
	mkdir -p $outputdir
	outputfile=$outputdir/$filename.json
	echo generating... $outputfile
    slither $path --json $outputfile
}

# Read the CSV file line by line
while IFS=' ' read -r path pragma_version; do
    process_csv "$path" "$pragma_version"
done < "$CSV"
