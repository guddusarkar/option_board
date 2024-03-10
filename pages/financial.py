import pandas as pd
import streamlit as st
st.title("Financial statments")
tab1, tab2,tab3,tab4,tab5 = st.tabs(["Balance sheet","P&L statment",'Q-o-Q P&L statment', 'cashflow', 'Share holding'])
with st.sidebar.form('formes'):
    stock= st.text_input("write Company symble name")
    submitted = st.form_submit_button("Submit")
    if submitted:
        try:
            tables= pd.read_html(f"https://www.screener.in/company/{stock}/consolidated/")
        except:
            tables = pd.read_html(f"https://www.screener.in/company/{stock}/")
        with tab1:
            st.subheader('Y-o-Y Balance sheet')
            st.dataframe(tables[6])
        with tab2:
            st.subheader('Y-o-Y Profit and Loss statment')
            st.dataframe(tables[1])
        with tab3:
            st.subheader('Q-o-Q Profit and Loss statment')
            st.dataframe(tables[0])
        with tab4:
            st.subheader('Y-o-Y Cash folw statment')
            st.dataframe(tables[7])
        with tab5:
            st.subheader('Owner Share holding Pattern')
            st.dataframe(tables[9])

# url= "https://www.chittorgarh.com/report/latest-buyback-issues-in-india/80/tender-offer-buyback/"
# data= pd.read_html(url)
# print