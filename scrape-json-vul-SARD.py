from urllib.request import urlopen
import json
import time
import argparse




def main():        
    parser = argparse.ArgumentParser(description='Scrape SARD dataset.')
    parser.add_argument('--max', type=int, default=2, help='Maximum number of pages to scrape')
    args = parser.parse_args()

    maxpage = args.max
    
    for i in range(1, maxpage+1):
        urlSARD = "https://samate.nist.gov/SARD/api/test-cases/search?language%5B%5D=java&state%5B%5D=bad&page="+str(i)+"&limit=100"
        page = urlopen(urlSARD)
        response = page.read()
        results = json.loads(response)
        
        with open(f'vulnerable/scraped_data_page_{i}.json', 'w') as outfile:
            json.dump(results, outfile, indent=4)
        time.sleep(5)



if __name__ == "__main__":
    data = main()
    