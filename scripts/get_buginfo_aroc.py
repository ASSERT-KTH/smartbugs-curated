import sys
import re
import json
import os

def get_contract_names_and_lines(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.readlines()
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return []

    contracts = []

    contract_pattern = re.compile(r'^\s*contract\s+(\w+)\b')

    for i, line in enumerate(content, start=1):
        match = contract_pattern.search(line)
        if match:
            contract_name = match.group(1)
            contracts.append((contract_name, i))

    return contracts

def get_contracts_for_lines(file_path, line_numbers):
    contracts = get_contract_names_and_lines(file_path)
    vuln_contracts = {}
    for line_number in line_numbers:
        for i in range(len(contracts) -1, -1, -1):
            print(contracts[i])
            if contracts[i][1] < line_number:
                if contracts[i][0] in vuln_contracts:
                    vuln_contracts[contracts[i][0]].append(line_number)
                else:
                    vuln_contracts[contracts[i][0]] = [line_number]
                break
    return vuln_contracts

def get_vuln_contract_name(directory, file_path, bug_type):
    base_name = os.path.basename(file_path)
    base_name = os.path.splitext(base_name)[0]
    vulnerable_lines = []
    with open(file_path, 'r') as file:
        for line in file:
            if '@vulnerable_at_lines' in line:
                vulnerable_lines.extend(map(int, re.findall(r'\d+', line)))

    if vulnerable_lines:
        vuln_contracts = get_contracts_for_lines(file_path, vulnerable_lines)
        if vuln_contracts:
            # Write the output to a csv file
            output_file = os.path.join(directory, 'BugInfo.csv')
            with open(output_file, 'a') as file:
                for contract_name in vuln_contracts:
                    file.write(f"{base_name} {contract_name}")
                    for line_number in vuln_contracts[contract_name]:
                        file.write(f" {line_number}/{bug_type}")
                    file.write('\n')
        else:
            print("No contracts found containing the vulnerable lines.")
    else:
        print("No vulnerable lines found in the file.")


def process_directory(directory, bug_type):
    for filename in os.listdir(directory):
        if filename.endswith('.sol'):
            file_path = os.path.join(directory, filename)
            print(f"Processing {file_path}")
            get_vuln_contract_name(directory, file_path, bug_type)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <directory> <bugtype>")
        sys.exit(1)

    dataset_directory = sys.argv[1]
    if not os.path.isdir(dataset_directory):
        print(f"Directory not found: {dataset_directory}")
        sys.exit(1)
    
    bug_type = sys.argv[2]

    process_directory(dataset_directory, bug_type)
