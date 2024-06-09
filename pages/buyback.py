# import all importent library
import streamlit as st
import requests
import pandas as pd
from datetime import datetime,timedelta
from bs4 import BeautifulSoup


# create titel of the page
st.title(':blue[upcomming] :red[Buy-back] list')


# extract data from website using requests library
url = "https://www.chittorgarh.com/report/latest-buyback-issues-in-india/80/tender-offer-buyback/"
response = requests.get(url)


# using beautifulsoup libratry to find table content
soup = BeautifulSoup(response.content, 'html.parser')
table = soup.find('table',class_="table table-bordered table-striped table-hover w-auto")
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
    df=df.drop(columns=['Compare','Buyback Type'])
    date_col=['Record Date', 'Issue Open', 'Issue Close']
    num_col=['BuyBack price (Per Share)','Current Market Price','Issue Size - Shares (Cr)','Issue Size - Amount (Cr)']
    df[date_col] = df[date_col].apply(pd.to_datetime,format='%b %d, %Y')
    df[num_col] = df[num_col].replace('', 0)
    df[num_col]=df[num_col].astype(float)
    df['expected Profit']=df['BuyBack price (Per Share)']-df['Current Market Price']
    current_date= datetime.now()+timedelta(hours=5, minutes=30)
    df = df.loc[(df['Record Date'] >= current_date-timedelta(days=30)) | (df['Record Date'].isna())]
    df.fillna('Not Published', inplace=True)
    df=df.set_index('Company Name')
    pd.set_option('display.expand_frame_repr', False)
    new_col=['BuyBack price (Per Share)','Current Market Price','Issue Size - Amount (Cr)','expected Profit']
    df[new_col]=df[new_col].astype('int')
    # Print the DataFrame in streamlit as table
    st.table(df.style.bar(subset=['Issue Size - Shares (Cr)'],color='#5fba7d',height=25))
    st.write('* in calculation of :blue[Expected Profit] we ignore application and others charges  ** approx charges in Zerodh Rs 30** ')
else:
    st.text("No table found on the website.")
