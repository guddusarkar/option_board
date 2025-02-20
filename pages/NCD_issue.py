# install important libraries
import requests
import streamlit as st 
from bs4 import BeautifulSoup
import pandas as pd

# page configaration
st.set_page_config(
    page_title="sumancapz",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded")

# page header
st.header(":blue[Current] :red[NCD]s (**Non Convertible Debentures**)")

# fatch data from ipowatch.com and create table
url='https://ipowatch.in/latest-ncd-issue-bonds-india/'
response=requests.get(url)
sup=BeautifulSoup(response.text,'html.parser')
#find table in the page
table=sup.find('table')

# Extract data
data = []
for row in table.find_all("tr")[1:]:  # Skip header row
    cols = row.find_all("td")
    if cols:
        company = cols[0].text.strip()
        open_date = cols[1].text.strip()
        close_date = cols[2].text.strip()
        size = cols[3].text.strip()
        link = cols[0].find("a")["href"] if cols[0].find("a") else None  # Extract link if present
        data.append([company, open_date, close_date, size, link])

# Create DataFrame
df = pd.DataFrame(data, columns=["Company", "Open", "Close", "Size", "URL"])

# Display DataFrame
if df.shape[0]>7:
    df= df[:7]
else: df
# display the table in streamlit page
formats = {'URL': st.column_config.LinkColumn("Details", display_text="click")}
st.dataframe(df,hide_index=True,column_config=formats)
# provide some details about NCD and selection process
st.divider()
st.subheader("What is Non Convertible Debentures (NCDs)?")
st.markdown("Non-convertible debentures (NCD) are fixed-income instruments, usually issued by high-rated companies in the form of a public issue to accumulate long-term capital appreciation. They offer relatively higher interest rates")
st.subheader("How to select NCD?")
st.markdown("You can invest when the company announces NCDs or purchase after it trades on the secondary market. You must check the company’s credit rating, issuer credibility and the coupon rate of the NCD. It would help if you purchase NCDs of a higher rating such as AAA+ or AA+.")


