# install importent libraries
import streamlit as st
import requests
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime,timedelta

#configaration of page
st.set_page_config(
    page_title="sumancapz",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded")

# create titles of the page
st.title('upcomming :red[IPO] and :gray[GMP]')

# extract data from investorgain.com using requests library
url1="https://sensexindia.in/calendar/ipo-calendar.aspx"
d1= requests.get(url1)

# use beautifulsoup to find data table
ta=BeautifulSoup(d1.content, 'html.parser')
table = ta.find('table', class_="table table-responsive Sensex_Table_2")
if table:
    # Extract data from the table
    rows = table.find_all('tr')
    table_data = []

    for row in rows:
        columns = row.find_all(['td', 'th'])
        row_data = [column.get_text(strip=True) for column in columns]
        table_data.append(row_data)

    # Remove any empty rows from the table data
    table_data = [row for row in table_data if any(row)]

    # Convert the table data into a DataFrame
    df = pd.DataFrame(table_data[1:], columns=table_data[0])
    df['IPO/SME']= df['IPO/SME'].apply(lambda x: 'Main Board' if 'IPO' in x else 'SME')
    df["Company"] = df["IPO"].str.replace(r'(Upcomin|Open|Close).*', '', regex=True)
    df['GMP%'] = df['Est Listing'].str.extract(r'\((.*?)\)')
    df['Listing Date'] = df['Listing Date'].apply(pd.to_datetime,format="%d %b %Y",errors='coerce')
    df['day']=df['Listing Date'].dt.day
    df['month']=df['Listing Date'].dt.month
    current_date= datetime.now()+timedelta(hours=5, minutes=30)   # current datetime in India
    df['Listing Date'] = df['Listing Date'].dt.strftime('%d-%b')
    df = df[(df['day'] == current_date.day) & (df['month'] == current_date.month)]
    df=df.rename(columns={'IPO':'Company'})
    df= df[['Company', 'Price', 'GMP Price','GMP%', 'Est Listing','Open Date', 'Close Date', 'BoA Date', 'Listing Date']]    
    df=df.set_index('Company')
    
    # Print the DataFrame streamlit page
    st.table(df)
    st.write(':blue[GMP]= Gray Market Premium, which representing expencted listing gain')
else:
    st.text("No upcomming available")
