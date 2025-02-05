import json
from pathlib import Path
import csv
import argparse

def list_files_in_folder(folder_path):
    path = Path(folder_path)
    return [str(file) for file in path.glob('**/*') if file.is_file()]

# Function to extract all unique zip urls
def extract(folder_path, output):
    # Define the CSV file path
    with open(output, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['cwe', 'download_url'])
        jsonfolder = list_files_in_folder(folder_path)
        for filename in jsonfolder:
            data = json.load(open(filename))
            for entry in data.get('testCases', []): 
                downloadurl = entry.get('download')
                for d in entry.get('sarif').get('runs', []):
                    for cwe in d.get('results', []):
                        if not cwe.get('ruleId') or cwe.get('ruleId').lower() == 'none':
                            cwe_code = d.get('properties').get('description').split(':')[0]
                        else:
                            cwe_code = cwe.get('ruleId')
                        writer.writerow([cwe_code, downloadurl])
            print(f"{filename}, exported")

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Extract data from JSON files and export to CSV.')
    parser.add_argument('--json_path', type=str, required=True, help='Path to the folder containing JSON files')
    parser.add_argument('--output', type=str, required=True, help='Path to the output CSV file')
    args = parser.parse_args()


    extract(folder_path=args.json_path,output=args.output)
    

if __name__ == "__main__":
    main()