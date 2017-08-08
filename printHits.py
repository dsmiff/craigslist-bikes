import os
import requests
import argparse
from pprint import pprint
from bs4 import BeautifulSoup

##_______________________________________________________||
parser = argparse.ArgumentParser()
parser.add_argument("-l", "--location", type=str, help="Location")
args = parser.parse_args()

##_______________________________________________________||
page = 'https://{0}.craigslist.org/search/bia'.format(args.location)
raw = requests.get(page).text
soup = BeautifulSoup(raw,'lxml')

##_______________________________________________________||
def main():

    title = soup.title.text

    results =  soup.find_all('li',class_='result-row')
    data = {}

    for result in results:
        key = result.a.get_text().encode('ascii', 'ignore').replace('\n','')
        data[key] = {}
        data[key]['link'] = result.a['href']
        data[key]['description'] = result.find('a',class_='result-title hdrlnk').text
        
    return data

if __name__=='__main__':
    data = main()
    pprint(data)
