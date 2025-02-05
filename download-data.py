import pandas as pd
import requests
import time
import os
import argparse

def download_files(csv_path, download_folder):
    # Load the CSV file into a pandas DataFrame
    df = pd.read_csv(csv_path)

    # Ensure the download folder exists
    os.makedirs(download_folder, exist_ok=True)

    # Loop through the download_url column
    for index, row in df.iterrows():
        download_url = row['download_url']
        file_name = os.path.join(download_folder, os.path.basename(download_url))

        # Download the file
        response = requests.get(download_url)
        with open(file_name, 'wb') as file:
            file.write(response.content)

        print(f"Downloaded {file_name}")

        # Cool down for 2 seconds
        time.sleep(2)

if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Download files from URLs in a CSV file.')
    parser.add_argument('--csv_path', type=str, required=True, help='Path to the CSV file')
    parser.add_argument('--download_folder', type=str, required=True, help='Path to the download folder')
    args = parser.parse_args()

    download_files(args.csv_path, args.download_folder)