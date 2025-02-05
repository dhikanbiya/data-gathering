from urllib.request import urlopen
import json
import time
import argparse




def main():        
    parser = argparse.ArgumentParser(description='Scrape SARD dataset.')    
    parser.add_argument('--state', type=str, required=True, help='State')
    parser.add_argument('--language', type=str, required=True, help='Language')    
    parser.add_argument('--output', type=str, default='not_vulnerable', help='output folder')
    args = parser.parse_args()

    
    state = args.state.lower()
    lang = args.language.lower()


    urlSARD = "https://samate.nist.gov/SARD/api/test-cases/search?language%5B%5D="+lang+"&state%5B%5D="+state+"&page=1&limit=100"
    page = urlopen(urlSARD)
    response = page.read()
    results = json.loads(response)
    totalpage = results['pageCount']    
    
    print("Total pages:", totalpage)
    
    
    for i in range(1, totalpage+1):
        urlSARD = "https://samate.nist.gov/SARD/api/test-cases/search?language%5B%5D="+lang+"&state%5B%5D="+state+"&page="+str(i)+"&limit=100"
        page = urlopen(urlSARD)
        response = page.read()
        results = json.loads(response)
       
        outfile = args.output
        with open(f'{outfile}/scraped_data_page_{i}.json', 'w') as outfile:
            json.dump(results, outfile, indent=4)
            print("Page", i, "done")
        print("Sleeping for 5 seconds")
        time.sleep(5)



if __name__ == "__main__":
    data = main()
    print("Data scraped successfully")
