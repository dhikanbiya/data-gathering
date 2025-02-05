# A small script for gathering data from SARD dataset

This script only working with vulnerable java source code dataset from SARD (for now)
```
https://samate.nist.gov/SARD/api/test-cases/search?language%5B%5D=java&state%5B%5D=bad&page="+{MAXIMUMPAGE}+"&limit=100
```

### How to use
- Scrape data using `scrape-json-vul-SARD`
 ```
 scrape-json-vul-SARD.py --max maximum-page-from-api
 ```
- `extract-data` to extract the json file into csv
for `extract-data` use this command:
```
python extract-data.py --json_path=vulnerable --output=csv/output.csv
```
