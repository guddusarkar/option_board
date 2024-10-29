# install importent libraries
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

# page configaration
st.set_page_config(
    page_title="sumancapz",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded")

# create titles of the page
st.title(':blue[Financial] freedom :gray[Calculator:]')

col1,col2= st.columns(2) 
with col1 :
    age= st.select_slider('Current Age :red[*]',help= 'put your current age',options=range(0,101))
    current_net_worth= st.number_input('Current Net worth', help= 'enter your current Assets or investment valuation',placeholder='current property value',value= None)
    monthly_salary= st.number_input('Monthly total income after Tax :red[*]', help= 'enter your current monthly income (all income less income tax)',placeholder='monthly income after tax',value= None)
    monthly_investment= st.number_input('Monthly investment persentage (%) on income :red[*]',help= 'put your monthly saving or investment value',
                                 placeholder='total monthly investment in %',value= None)
    return_on_investment= st.select_slider('Expected return on investment percentage (%) :red[*]',help= 'Put you expected CAGR on your investment or savig amount',options=range(0,101))
with col2:
    retired_age= st.select_slider('Retirement Age :red[*]',options=range(0,101), help= 'put your expected Rerirment age')
    monyhly_expenses= st.number_input('Average monthly expenses :red[*]',help= 'enter your current average monthly expenses (you can put 3 month average expenses).',
                                      placeholder='Monthly average household expenses',value= None)
    Annual_salary_growth = st.select_slider('Annual Income Growth rate (%) :red[*]',help= 'Put you yearly Salary growth',options=range(0,101))
    inflation_rate= st.number_input('Expected inflation rate (%) :',help= 'Put WPI or CPI increasing rage. in Indaia inflation rate normally lies between 6% -8%',value=7)
    FF_mulipal= st.number_input('Financial Freedom Multiplyer',
                                    help= 'how much multipul amount you need that can take care of you monthly expenses in future. acording to most of the financial advise it should be 30. if you are not satisfied with you current life style and want to increase household expenses, you can consider multilpyer in higher side',
                                    value= 30)


if st.button("submit",type="primary"):
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
    final= data[['salary','investment', 'FF_value','net_worth']]

    def colour_outliers(val):
        if val >= FF_amount:
            return 'background-color: lightgreen; font-weight: bold; color: black'
        else:
            return ''
    
    if f_data.empty:
        st.subheader('**You are not able to get Financially free before your retiredment** \U0001F612',divider='rainbow')
    else:
        FF_year=f_data.index.min()
        FF_amount=f_data.iloc[0,5]
        your_age= FF_year + age 
        st.subheader(f'you get Financial Freedom after {FF_year} years and your age would be {your_age}  🤑')
        st.subheader(f'At that time your net worth would be ₹ {FF_amount}  💵💰',divider='rainbow')

    st.subheader('Net worth Vs. Financial Freedom Value')
    fig, ax = plt.subplots(figsize=(19, 9))
    
    ax.plot(data['net_worth'],label= 'net worth')
    ax.plot(data['FF_value'], label= 'Freedom value')
    ax.legend(['Net worth', 'Financial Freedom value'])
    ax.set_xlabel('Years',labelpad=5,fontsize='xx-large')
    ax.set_ylabel('Amount',labelpad=5,fontsize='xx-large')
    try:
        ax.vlines(FF_year,ymin= 0,ymax= data['net_worth'].max(),linestyles='dashed',label='Financial free year',colors='black')
        ax.text(2,data['net_worth'].quantile(.95),f'you get Financial Freedom after {FF_year} years',bbox=dict(facecolor='skyblue', alpha=0.5))
    except:
        pass
    
   
    st.pyplot(fig,use_container_width=True)
    # st.line_chart(data,y=['net_worth','FF_value'],x_label='year', y_label= 'Amount',color=["#f0f", "#04f"])
    st.subheader('Detalis information')
    try:
        st.table(final.style.applymap(colour_outliers,subset=['net_worth']))
    except:
        st.table(final)
