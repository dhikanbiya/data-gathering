# A small script for gathering data from SARD dataset

Please see the `status` and `language` in SARD Documentation
```
https://samate.nist.gov/SARD/documentation#search
```

### How to use
Scrape data using `scrape-json-vul-SARD` and store in json file for each page
 ```
 python scrape-json-vul-SARD.py  --state={state} --language={programming language} --output={json output folder}
 ```
`extract-data` the json file into csv
```
python extract-data.py --json_path={folder path to json file} --output={place where to store csv, dont forget to include the file extension}
```
`download_data` to download file and store on the directory, each download will pause 2 seconds
```
python download_data.py --csv_path={path to csv file} --download_folder={path to folder}
```
