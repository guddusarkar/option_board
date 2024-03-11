# import all importent library
import streamlit as st
import requests
import pandas as pd
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

    # Print the DataFrame in streamlit as table
    st.table(df)
else:
    st.text("No table found on the website.")
