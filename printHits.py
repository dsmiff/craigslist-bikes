import os
import json
import requests
import argparse
from pprint import pprint
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from forex_python.converter import CurrencyRates

##_______________________________________________________||
parser = argparse.ArgumentParser()
parser.add_argument("-l", "--location", nargs ="*", type=str, help="Location")

##_______________________________________________________||
def returnConversion(location):
    c = CurrencyRates()
    with open('common_currencies.json') as currency_file:
        currencies = json.load(currency_file)
    for code, info in currencies.iteritems():
        if info['capital'] == location:
            conversion = c.get_rate(code, 'EUR')
            break
        else:
            conversion = 1.

    return conversion

##_______________________________________________________||
def meanPrice(data, locations):
    # Convert prices from strings to ints
    for location in locations:
        prices = [int(price) for price in data[location].keys()]

        # Convert prices list to numpy array
        prices_array = np.asarray(prices)
        sns_plot = sns.distplot(prices_array,kde=False,bins=20,label=location)
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
        conversion = returnConversion(location)
        
        for result in results:
            price = result.a.get_text().encode('ascii', 'ignore').replace('\n','')
            if not price: continue
            price = str(int(float(price)*conversion))
            data[location][price] = {}
            data[location][price]['link'] = result.a['href']
            data[location][price]['description'] = result.find('a',class_='result-title hdrlnk').text

        df = pd.DataFrame(data[location].items(),columns=['Price','Info'])
        df['Price'] = pd.to_numeric(df['Price']).fillna(value=0)

    meanPrice(data, args.location)

    return data

if __name__=='__main__':
    data = main()
    #pprint(data)
