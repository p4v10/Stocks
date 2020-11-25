# Streamlit Stock App

#Imports
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import yfinance as yf

#Page title and icon
st.set_page_config(page_title='Stocks Graphs', page_icon='chart_with_upwards_trend')

#Scraping data
@st.cache
def load_sp_data():
    url= 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    html = pd.read_html(url, header = 0)
    sp_df = html[0]
    return sp_df


sp_df = load_sp_data()

#grouping data by sector
sector = sp_df.groupby('GICS Sector')

#sidebar
sort_sector_unq = sorted(sp_df['GICS Sector'].unique())
select_sector = st.sidebar.multiselect('Sector', sort_sector_unq)

#filter data
df_select_sector = sp_df[(sp_df['GICS Sector'].isin(select_sector))]



st.write("""
Stock Trends for 2019
""")


st.sidebar.header('Chose Something')
