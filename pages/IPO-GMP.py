# install importent libraries
import streamlit as st
import pandas as pd
from datetime import datetime,timedelta

#configaration of page
st.set_page_config(
    page_title="sumancapz",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded")

# create titles of the page
st.title('upcomming :red[IPO] and :gray[GMP]')


try:
    # extract data from ipodekho.com using requests library
    gmp= pd.read_html('https://ipodekho.in/ipo-gmp-grey-market-premium/')[0]
    ipo= pd.read_html('https://ipodekho.in/')[0]
    ipo[['GMP','Profit %']]=gmp[['GMP','Profit %']]
    ipo["Company"] = ipo["Name"].str.replace(r'(Upcomin|Live|Last|List|Waiting|Allotment).*', '', regex=True)
    ipo['Close'] = ipo['Close'].apply(pd.to_datetime,format="%d %b, %Y",errors='coerce')
    current_date= datetime.now()-timedelta(days=5) # 5 day before current date
    ipo=ipo[ipo['Close']>=current_date]
    ipo['Close'] = ipo['Close'].dt.strftime('%d %b, %Y')
    df=ipo[["Company","Type","Open","Close","GMP","Profit %","Lot Price"]]#.set_index('Company')
    df = df.sort_values(by="Close", ascending=False)
    # Print the DataFrame streamlit page
    st.dataframe(df,hide_index= True)
    st.write(':blue[GMP]= Gray Market Premium, which representing expencted listing gain')
except:
    st.text("No upcomming IPO available")
