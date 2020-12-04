# Import Python Libraries
from bs4 import BeautifulSoup
import requests
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from IPython.core.interactiveshell import InteractiveShell

# allowing multiple printing output
InteractiveShell.ast_node_interactivity = "all"

# Dictionary with urls and keys
urls = dict()
urls['BTC'] = "https://coinmarketcap.com/currencies/bitcoin/historical-data/?start=20130428&end=20201203"
urls['BCH'] = "https://coinmarketcap.com/currencies/bitcoin-cash/historical-data/?start=20130428&end=20201203"
urls['ETH'] = "https://coinmarketcap.com/currencies/ethereum/historical-data/?start=20130428&end=20201203"
urls['XRP'] = "https://coinmarketcap.com/currencies/ripple/historical-data/?start=20130428&end=20201203"
urls['LTC'] = "https://coinmarketcap.com/currencies/litecoin/historical-data/?start=20130428&end=20201203"


coins_df = dict()


#Loop on names and urls
for (name, url) in urls.items():
    content = requests.get(url).content
    soup = BeautifulSoup(content,'html.parser')
    table = soup.find('table',{'class': 'table'})
    data = [[td.text.strip() for td in tr.findChildren('td')] for tr in table.findChildren('tr')]
    df = pd.DataFrame(data) #creating dataframe
    df.drop(df.index[0], inplace=True) #empty 1st row
    df[0] = pd.to_datetime(df[0]) #indexing time
    for i in range(1,7):
        df[i] = pd.to_numeric(df[i].str.replace(",","").str.replace("-",""))
        df.columns = ['Date','Open ' + name, 'High ' + name,'Low ' + name, 'Close ' + name, 'Volume ' + name,'Market Cap ' + name] #defining column names
        df.set_index('Date',inplace=True)
        df = df.drop(columns = ['Open ' + name,'High ' + name, 'Low ' + name])
        df.to_csv(name + '_price.csv') # save data of the coin in csv
        coins_df[name] = df

st.write(coins_df['BTC'].head(10))
