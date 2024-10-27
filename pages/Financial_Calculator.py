# install importent libraries
import streamlit as st
import pandas as pd
import numpy as np

# create titles of the page
st.title(':blue[Financial] freedom :gray[Calculator]')

col1,col2= st.columns(2) 
with col1 :
    age= st.select_slider('Current Age :red[*]',help= 'put your current age',options=range(0,101))
    current_net_worth= st.number_input('Current Net worth', help= 'enter your current Assets or investment valuation',placeholder='current property value')
    monthly_salary= st.number_input('Monthly total income after Tax :red[*]', help= 'enter your current monthly income (all income less income tax)',placeholder='monthly income after tax')
    monthly_investment= st.number_input('Monthly investment persentage (%) on income :red[*]',help= 'put your monthly saving or investment value',
                                 placeholder='total monthly investment in %')
    return_on_investment= st.select_slider('Expected return on investment percentage (%) :red[*]',help= 'Put you expected CAGR on your investment or savig amount',options=range(0,101))
with col2:
    retired_age= st.select_slider('Retirement Age :red[*]',options=range(0,101), help= 'put your expected Rerirment age')
    monyhly_expenses= st.number_input('Average monthly expenses :red[*]',help= 'enter your current average monthly expenses (you can put 3 month average expenses).',
                                      placeholder='Monthly average household expenses')
    Annual_salary_growth = st.select_slider('Annual Income Growth rate (%) :red[*]',help= 'Put you yearly Salary growth',options=range(0,101))
    inflation_rate= st.number_input('Expencted inflation rate (%) :',help= 'Put WPI or CPI increasing rage. in Indaia inflation rate normally lies between 6% -8%',value=7)
    FF_mulipal= st.number_input('Financial Freedom Multiplyer',
                                    help= 'how much multipul amount you need that can take care of you monthly expenses in futur. acording to most of the financial advise it should be 30. if you are not satisfied with you current life style and want to increase household expenses, you can consider multilpyer in higher side',
                                    value= 30)


if st.button("submit",type="primary"):
    try:
        age_of_service = retired_age-age
        annula_salary= monthly_salary*12
        annula_investment= int((monthly_salary*(monthly_investment/100))*12)
        annula_expenses= monyhly_expenses*12
        data= pd.DataFrame()
        data['age']= np.arange(1,age_of_service+1)
        data.set_index('age',inplace=True)
        salary=[]
        salary.append(int(annula_salary))
        for i in range(2,age_of_service+1):
            salary.append(int(annula_salary*(1+Annual_salary_growth/100)**(i-1)))
        data['salary']= salary
        data['investment']= data['salary']*monthly_investment/100
        data['year_investment_value']=((data['investment']*return_on_investment/100)*6.5/12)+data['investment']
        FF_value=[]
        for i in range(1,age_of_service+1):
            FF_value.append(int(FF_mulipal*annula_expenses*(1+inflation_rate/100)**(i)))
        data['FF_value']=FF_value
        sum=[]
        sum.append(data['year_investment_value'][1])
        for i in range(2,age_of_service+1):
            sum.append((sum[-1]*(1+return_on_investment/100))+(data['investment'][i]*(return_on_investment/100*6.5/12)+data['investment'][i]))
        data['sum']= sum
        data['sum']=data['sum'].astype(int)
        data['year_investment_value']=data['year_investment_value'].astype(int)
        data['investment']=data['investment'].astype(int)
        old_valuation=[]
        for i in range(1,age_of_service+1):
            old_valuation.append(int(current_net_worth*(1+return_on_investment/100)**(i)))
        data['net_worth']= old_valuation+data['sum']
        f_data= data[data['net_worth']>=data['FF_value']]
        FF_year=f_data.index.min()
        FF_amount=f_data.iloc[0,5]


        def colour_outliers(val):
            if val >= FF_amount:
                return 'background-color: lightgreen; font-weight: bold; color: black'
            else:
                return ''
        if f_data.empty:
            st.text('You are not able to get Financially free before your retiredment')
        else:
            st.text(f'you get Financial Freedom after {FF_year} years')
            st.text(f'and At that time your net worth would be {FF_amount}')
        st.subheader('Net worth Vs. Financial Freedom Value')
        st.line_chart(data,y=['net_worth','FF_value'],x_label='year', y_label= 'Amount',color=["#f0f", "#04f"])
        st.subheader('Detalis information')
        st.table(data.style.applymap(colour_outliers,subset=['net_worth']))
    except:
        st.text('please provide acurate information')
