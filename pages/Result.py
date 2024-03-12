# installing important libraries
import streamlit as st
import pandas as pd

# adding title of the page
st.title(':red[Quaterly Result] for :blue[Today]')


# extracting todays result announcement data from economicstimes website 
try
  d=pd.read_html("https://economictimes.indiatimes.com/markets/stocks/mcalendar.cms")
  st.table(d[0])
except
  st.text(' ** NOT RESULT ANNOUNCED TODAY**')
