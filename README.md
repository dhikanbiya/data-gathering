# A small script for gathering data from SARD dataset

Please see the `status` and `language` in SARD Documentation
```
https://samate.nist.gov/SARD/documentation#search
```

### How to use
- Scrape data using `scrape-json-vul-SARD`
 ```
 python scrape-json-vul-SARD.py  --state={state} --language={programming language} --output={json output folder}
 ```
- `extract-data` the json file into csv
```
python extract-data.py --json_path=vulnerable --output=csv/output.csv
```
