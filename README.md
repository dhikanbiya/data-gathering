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
`extract-zip` extract all the zip file in folder to destination folder, remove other files that not relevant to programming languange that will use
```
python extract-zip.py --source_folder={folder that contain all zip file} --destination_folder={extracted folder} --exclude_extension={file extension to exclude ex: .java}
```
Extract cpg and ast as json file using joern client - https://github.com/joernio/cpgqls-client-python
```
python joernclient.py --base_folder {folder containing the source code}    
```

## Joern script
Make sure to start the joern server:
```
joern --server --server-host localhost --server-port 8088
```

Use this command to generate json for ast or cfg from the source code
```
joern-parse /src/directory
joern --script script/exportCPG.sc --param cpgFile={cpg location} --param outFile={output file}
```

