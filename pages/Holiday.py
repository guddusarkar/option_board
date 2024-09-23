# import important libraries
import streamlit as st
import pandas as pd
import numpy as np
import requests

#configur the page
st.set_page_config(
    page_title="sumancapz",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded")

# input header of the page
st.header("Annual :blue[Holiday] list :sunglasses:")

# fatching data from NSE website
header = {
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "DNT": "1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.0.0",
    "Sec-Fetch-User": "?1", "Accept": "*/*", "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "cors",
    "Accept-Encoding": "gzip, deflate, br", "Accept-Language": "en-US,en;q=0.9,hi;q=0.8"
    }
def nse_urlfetch(url):
  r_session = requests.session()
  nse_live = r_session.get("http://nseindia.com", headers=header)
  return r_session.get(url, headers=header)
try:
  data= nse_urlfetch("https://www.nseindia.com/api/holiday-master?type=trading").json()
  table= pd.DataFrame(data.get('CM'))
  table.columns= ['Date','Day','Description','SL no']
  table.drop(['SL no'],axis=1,inplace=True)
  table.set_index('Date',inplace=True)  
  st.table(data= table)
except:
  st.text('error to fatching data from site')
