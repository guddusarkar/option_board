import streamlit as st
import pandas as pd
st.title('announcement of result')
d=pd.read_html("https://economictimes.indiatimes.com/markets/stocks/mcalendar.cms")
st.dataframe(d[0])
