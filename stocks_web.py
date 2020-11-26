# Streamlit Stock App

#Imports
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
import yfinance as yf
import base64

#Page title and icon
st.set_page_config(page_title='Stocks Graphs', page_icon='chart_with_upwards_trend')

#Scraping data
@st.cache
def load_sp_data():
    url= 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header = 0)
    sp_df = html[0]
    return sp_df

st.write("""
Stock Trends for 2019
""")


sp_df = load_sp_data()

#grouping data by sector
sector = sp_df.groupby('GICS Sector')

st.sidebar.header('Chose Something')

#sidebar
sort_sector_unq = sorted(sp_df['GICS Sector'].unique())
select_sector = st.sidebar.multiselect('Sector', sort_sector_unq, default='Energy')

#filter data
df_select_sector = sp_df[(sp_df['GICS Sector'].isin(select_sector))]


#select_sector2 = st.sidebar.multiselect('Symbol', df_select_sector)




st.header('Display Companies in Selected Sector')
st.write('Data Dimension: ' + str(df_select_sector.shape[0]) + ' rows and ' + str(df_select_sector.shape[1]) + ' columns.')
st.dataframe(df_select_sector)

#donwload s%p500
def downloadfile(sp_df):
    csv = sp_df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode() #bites convertion
    href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
    return href

st.markdown(downloadfile(df_select_sector), unsafe_allow_html=True)


#yfinance data
data = yf.download(
        tickers = list(df_select_sector[:10].Symbol),
        period = "ytd",
        interval = "1d",
        group_by = 'ticker',
        auto_adjust = True,
        prepost = True,
        threads = True,
        proxy = None
    )


#Plotting charts
def price_plot(symbol):
    sp_df = pd.DataFrame(data[symbol].Close)
    sp_df['Date'] = sp_df.index
    plt.fill_between(sp_df.Date, sp_df.Close, color='salmon', alpha=0.3)
    plt.plot(sp_df.Date, sp_df.Close, color='salmon', alpha=0.8)
    plt.xticks(rotation=90)
    plt.title(symbol, fontweight='bold')
    plt.xlabel('Date', fontweight='bold')
    plt.ylabel('Closing Price', fontweight='bold')
    return st.pyplot()

st.set_option('deprecation.showPyplotGlobalUse', False)


#Number of charts(client pick)
comp_n = st.sidebar.slider('Number of Companies', 1, 15)



if st.button('Show Plots'):
    st.header('Stock Closing Price')
    for i in list(df_select_sector.Symbol)[:comp_n]:
        price_plot(i)
