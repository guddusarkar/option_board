# importing importent libraries
import pandas as pd
import streamlit as st

# creating title and different tabs
st.title(":blue[Financial] statments")
tab1, tab2,tab3,tab4,tab5 = st.tabs(["Balance sheet","P&L statment",'Q-o-Q P&L statment', 'cashflow', 'Share holding'])

# creating sidebar and submit button
with st.sidebar.form('formes'):
    stock= st.text_input("write Company symble name")
    submitted = st.form_submit_button("Submit")
    if submitted:
        try:

            # fatch the financial data from screener.in website
            try:
                tables= pd.read_html(f"https://www.screener.in/company/{stock}/consolidated/")
            except:
                tables = pd.read_html(f"https://www.screener.in/company/{stock}/")
            with tab1:
                st.subheader('Y-o-Y Balance sheet')
                st.table(tables[6], index=False)
            with tab2:
                st.subheader('Y-o-Y Profit and Loss statment')
                st.table(tables[1], index=False)
            with tab3:
                st.subheader('Q-o-Q Profit and Loss statment')
                st.table(tables[0], index=False)
            with tab4:
                st.subheader('Y-o-Y Cash folw statment')
                st.table(tables[7], index=False)
            with tab5:
                st.subheader('Owner Share holding Pattern')
                st.table(tables[9], index=False)
        except:
            st.text('please write correct symble')
