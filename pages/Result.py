# installing important libraries
import streamlit as st
import pandas as pd

#configaration of page
st.set_page_config(
    page_title="sumancapz",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded")

# adding title of the page
st.title(':red[Quaterly Result] for :blue[Today]')

# extracting todays result announcement data from economic-times website using requests library
url = "https://economictimes.indiatimes.com/markets/stocks/mcalendar.cms"
# Fatch the data using pandas read_html
table = pd.read_html(url)[0]
if table:
    df=table.set_index("Company Name")
    # Print the DataFrame
    st.table(df)
    st.divider()
    st.title("upcoming :red[Result]")
    result= pd.read_html("https://www.livemint.com/market/quarterly-results-calendar")[0]
    result.set_index('STOCKS',inplace=True)
    st.table(result)
else:
    st.text(' ** NOT RESULT ANNOUNCED TODAY**')
