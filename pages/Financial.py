# importing importent libraries
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

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
                st.dataframe(tables[6], use_container_width= True, hide_index=True)
            with tab2:
                st.subheader('Y-o-Y Profit and Loss statment')
                st.dataframe(tables[1], use_container_width= True, hide_index=True)
            with tab3:
                st.subheader('Q-o-Q Profit and Loss statment')
                qpl=st.dataframe(tables[0], use_container_width= True, hide_index=True)
                #convart data into dataframe
                # qpl= pd.DataFrame(qpl.T)
                # qpl.drop(qpl.index[0], inplace=True)
                # qpl.columns= ['Sales', 'Expenses','Operating Profit', 'OPM%', 'Other income', 'Interest', 'Depreciation', 'PBT', 'Tax%','PAT','EPS','PDF']
                # qpl.drop(columns=['PDF','OPM%'],axis=1, inplace=True)

                # #edit some columns
                # nu_col= ['Sales','Expenses','Operating Profit','Other income',	'Interest',	'Depreciation',	'PBT','PAT']
                # qpl[nu_col]=qpl[nu_col].astype('int')
                # qpl['Growth%']=((qpl.Sales/qpl.Sales.shift(1))-1)*100
                # qpl['OPM%']= (qpl['Operating Profit']/qpl.Sales)*100

                # #ploting data
                # col1,col2= st.columns(2)
                # with col1:
                #     plt.figure(figsize=(12,4))
                #     plt.bar(x=qpl.index,height=qpl.Sales,width=0.5)
                #     plt.title('quaterly sales')
                # with col2:
                #     plt.figure(figsize=(12,4))
                #     plt.bar(x=qpl.index,height=qpl['Growth%'],width=0.5)
                #     plt.title('quaterly Sales Growth')
            with tab4:
                st.subheader('Y-o-Y Cash folw statment')
                st.dataframe(tables[7], use_container_width= True, hide_index=True)
            with tab5:
                st.subheader('Owner Share holding Pattern')
                st.dataframe(tables[9], use_container_width= True, hide_index=True)
        except:
            st.text('please write correct symble')
