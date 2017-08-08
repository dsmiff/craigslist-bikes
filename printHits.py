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
parser.add_argument("-l", "--location", type=str, help="Location")
args = parser.parse_args()

##_______________________________________________________||
if not args.location:
    print "Please provide an input location"
page = 'https://{0}.craigslist.org/search/bia'.format(args.location)
raw = requests.get(page).text
soup = BeautifulSoup(raw,'lxml')

##_______________________________________________________||
def meanPrice(data, location):
    # Convert prices from strings to ints
    prices = [int(price) for price in data.keys()]

    # Convert prices list to numpy array
    prices_array = np.asarray(prices)
    sns_plot = sns.distplot(prices_array,kde=False, color="b",label=location)
    plt.xlabel('bike price (euros)')
    plt.ylabel('mean occurances')
    plt.legend()
    plt.savefig('prices.png')

##_______________________________________________________||
def main():

    title = soup.title.text
    results =  soup.find_all('li',class_='result-row')
    data = {}

    for result in results:
        key = result.a.get_text().encode('ascii', 'ignore').replace('\n','')
        if not key: continue
        data[key] = {}
        data[key]['link'] = result.a['href']
        data[key]['description'] = result.find('a',class_='result-title hdrlnk').text
        
    meanPrice(data, args.location)
    df = pd.DataFrame(data.items(),columns=['Price','Info'])
    df['Price'] = pd.to_numeric(df['Price']).fillna(value=0)
    return data

if __name__=='__main__':
    data = main()
    #pprint(data)
