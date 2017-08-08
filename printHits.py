import os
import requests
import argparse
from pprint import pprint
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

##_______________________________________________________||
parser = argparse.ArgumentParser()
parser.add_argument("-l", "--location", nargs ="*", type=str, help="Location")

##_______________________________________________________||
def meanPrice(data, locations):
    # Convert prices from strings to ints
    for location in locations:
        prices = [int(price) for price in data[location].keys()]

        # Convert prices list to numpy array
        prices_array = np.asarray(prices)
        sns_plot = sns.distplot(prices_array,kde=False,label=location)
        plt.xlabel('bike price (euros)')
        plt.ylabel('mean occurances')
        plt.legend()
        plt.savefig('prices_{0}.png'.format(location))
    plt.savefig('prices_comp.png')
    
##_______________________________________________________||
def main():

    args = parser.parse_args()

    if not args.location:
        print "Please provide an input location"

    data = {}
        
    for location in args.location:
        page = 'https://{0}.craigslist.org/search/bia'.format(location)
        raw = requests.get(page).text
        soup = BeautifulSoup(raw,'lxml')

        title = soup.title.text
        results =  soup.find_all('li',class_='result-row')
        data[location] = {}
        
        for result in results:
            key = result.a.get_text().encode('ascii', 'ignore').replace('\n','')
            if not key: continue
            data[location][key] = {}
            data[location][key]['link'] = result.a['href']
            data[location][key]['description'] = result.find('a',class_='result-title hdrlnk').text

        df = pd.DataFrame(data[location].items(),columns=['Price','Info'])
        df['Price'] = pd.to_numeric(df['Price']).fillna(value=0)

    meanPrice(data, args.location)
    print data

    return data

if __name__=='__main__':
    data = main()
    #pprint(data)
