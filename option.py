# import all important libraries
import matplotlib.pyplot as plt
import requests
import numpy as np
import pandas as pd
import streamlit as st

#configaration of page
st.set_page_config(
    page_title="sumancapz",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded")

# add title of the web-app
st.title(':green[Suman Capz] **Option Dashboard**')
st.header('option analysis',divider='rainbow')

#create some tab for option analysis
tab1, tab2,tab3 = st.tabs(["option chain","OI",'Ratio strategy'])

#creathing data fatching engin from NSE website
default_header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"
}
header = {
            "referer": "https://www.nseindia.com/",
             "Connection": "keep-alive",
             "Cache-Control": "max-age=0",
             "DNT": "1",
             "Upgrade-Insecure-Requests": "1",
             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
             "Sec-Fetch-User": "?1",
             "Accept": "ext/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
             "Sec-Fetch-Site": "none",
             "Sec-Fetch-Mode": "navigate",
             "Accept-Language": "en-US,en;q=0.9,hi;q=0.8"
            }
def nse_urlfetch(url, origin_url="http://nseindia.com"):
    r_session = requests.session()
    nse_live = r_session.get(origin_url, headers=default_header)
    cookies = nse_live.cookies
    return r_session.get(url, headers=header, cookies=cookies)

def expiry_data(symbol):
    """
    get NSE option expiry datesfor the symbol
    :param symbol: eg:'TCS'/'BANKNIFTY'
    :return: list of expiry dates
    """

    origin_url = "https://www.nseindia.com/option-chain"
    exp = nse_urlfetch('https://www.nseindia.com/api/option-chain-contract-info?symbol=' + symbol,
                               origin_url=origin_url).json()
    return exp['expiryDates']
def time_price(index):
    """
    get update time and price for the symbol
    :param symbol: eg:'TCS'/'BANKNIFTY'
    :return: pandas dataframe
    """

    origin_url = "https://www.nseindia.com/option-chain"
    try:
        payload = nse_urlfetch(f'https://www.nseindia.com/api/option-chain-v3?type=Indices&symbol={index}&expiry={expiry_data(index)[0]}',
                                origin_url=origin_url).json()
    except:
        payload = nse_urlfetch(f'https://www.nseindia.com/api/option-chain-v3?type=Equity&symbol={index}&expiry={expiry_data(index)[0]}',
                                origin_url=origin_url).json()
    return payload['records']['timestamp'], payload['records']['underlyingValue']
def live_option_chain(index,exp_date):
  origin_url = "https://www.nseindia.com/option-chain"
  try:
      data = nse_urlfetch(f'https://www.nseindia.com/api/option-chain-v3?type=Indices&symbol={index}&expiry={exp_date}',
                              origin_url=origin_url).json()
  except:
      data = nse_urlfetch(f'https://www.nseindia.com/api/option-chain-v3?type=Equity&symbol={index}&expiry={exp_date}',
                               origin_url=origin_url).json()
  
  ce={}
  pe={}
  n=0
  m=0
  for i in data['records']['data']:
    # if i['expiryDate']==exp_date:
    try:
      ce[n]=i['CE']
      n=n+1
    except:
      pass
    try:
      pe[m]=i['PE']
      m=m+1
    except:
      pass
  ce_df= pd.DataFrame.from_dict(ce).transpose()
  ce_df.columns +='_CE'
  pe_df= pd.DataFrame.from_dict(pe).transpose()
  pe_df.columns += '_PE'
  option=pd.concat([ce_df,pe_df],axis=1)
  chain=option[['openInterest_CE','changeinOpenInterest_CE','impliedVolatility_CE','lastPrice_CE','strikePrice_CE','openInterest_PE','changeinOpenInterest_PE','impliedVolatility_PE','lastPrice_PE']]
  chain.columns=['CALLS_OI', 'CALLS_Chng_in_OI','IV_CE','CALLS_LTP','Strike_Price','PUTS_OI','PUTS_Chng_in_OI','IV_PE','PUTS_LTP']
  return chain

# create bar to select index instrument and for expiry day selection
c1, c2= st.columns(2)
index= c1.selectbox("select index name",('NIFTY',"BANKNIFTY","FINNIFTY"))
last_update, cmp =time_price(index)
ex= c2.selectbox('select expiry date',expiry_data(index))


try:
  option=live_option_chain(index,ex)
  o=option[['CALLS_OI', 'CALLS_Chng_in_OI','CALLS_LTP','Strike_Price','PUTS_LTP','PUTS_Chng_in_OI', 'PUTS_OI']].set_index('Strike_Price')

  if index =='NIFTY':
    range=(int(np.round(cmp / 50.0)) * 50)+1000,(int(np.round(cmp / 50.0)) * 50)-1000
    oi=o.loc[range[1]:range[0]]
  elif index == 'BANKNIFTY':
    range=(int(np.round(cmp/100.0)) *100)+1500,(int(np.round(cmp / 100.0)) * 100)-1500
    oi=o.loc[range[1]:range[0]]
  else:
      range = (int(np.round(cmp / 50.0)) * 50)+900,(int(np.round(cmp / 50.0)) * 50)-900
      oi = o.loc[range[1]:range[0]]
  with tab1:
    st.subheader('Option chain')
    st.text(f"Last Update : {last_update}")
    st.table(oi.style.highlight_max(axis=0,subset=['CALLS_OI','PUTS_OI','CALLS_Chng_in_OI','PUTS_Chng_in_OI']))
  with tab2:
    
    st.subheader('Open interest analysis')
    st.text(f"Last Update : {last_update}")
    fig, ax = plt.subplots(2, 1)
    ax[0].bar(oi.index, oi['CALLS_OI'], color='blue', width=20)
    ax[0].bar(oi.index - 10, oi['PUTS_OI'], color='red', width=20)
    ax[0].axvline(x=cmp, color='black', linestyle='--')
    ax[0].set_title('OI position')
    ax[1].bar(oi.index, oi['CALLS_Chng_in_OI'], color='blue', width=20)
    ax[1].bar(oi.index - 10, oi['PUTS_Chng_in_OI'], color='red', width=20)
    ax[1].axvline(x=cmp, color='black', linestyle='--')
    ax[1].set_xlabel('Change in OI')
    st.pyplot(fig)
  if index =="NIFTY":
    
    call = pd.DataFrame()
    call['CALLS 50 sprade'] = o['CALLS_LTP'] - ((o['CALLS_LTP'].shift(-1)) * 2)
    call['CALLS 100 sprade'] = o['CALLS_LTP'] - ((o['CALLS_LTP'].shift(-2)) * 2)
    call['CALLS 150 sprade'] = o['CALLS_LTP'] - ((o['CALLS_LTP'].shift(-3)) * 2)
    call['CALLS 200 sprade'] = o['CALLS_LTP'] - ((o['CALLS_LTP'].shift(-4)) * 2)
    call['CALLS 250 sprade'] = o['CALLS_LTP'] - ((o['CALLS_LTP'].shift(-5)) * 2)
    call['CALLS 300 sprade'] = o['CALLS_LTP'] - ((o['CALLS_LTP'].shift(-6)) * 2)
    call = call[call.index > cmp].dropna().iloc[:12]
    put = pd.DataFrame()
    put['PUTS 50 sprade'] = o['PUTS_LTP'] - ((o['PUTS_LTP'].shift(1)) * 2)
    put['PUTS 100 sprade'] = o['PUTS_LTP'] - ((o['PUTS_LTP'].shift(2)) * 2)
    put['PUTS 150 sprade'] = o['PUTS_LTP'] - ((o['PUTS_LTP'].shift(3)) * 2)
    put['PUTS 200 sprade'] = o['PUTS_LTP'] - ((o['PUTS_LTP'].shift(4)) * 2)
    put['PUTS 250 sprade'] = o['PUTS_LTP'] - ((o['PUTS_LTP'].shift(5)) * 2)
    put['PUTS 300 sprade'] = o['PUTS_LTP'] - ((o['PUTS_LTP'].shift(6)) * 2)
    put = put[put.index < cmp].dropna().iloc[-12:]
    ratio = pd.concat([put, call])

    def color_range(val):
        color = 'red' if 0.5 <= val <= 8 else 'black'
        return f'color: {color}'

    ratio = ratio.style.applymap(color_range)
   
  elif index== 'BANKNIFTY':
    
    call = pd.DataFrame()
    call['CALLS 100 sprade'] = o['CALLS_LTP'] - ((o['CALLS_LTP'].shift(-1)) * 2)
    call['CALLS 200 sprade'] = o['CALLS_LTP'] - ((o['CALLS_LTP'].shift(-2)) * 2)
    call['CALLS 300 sprade'] = o['CALLS_LTP'] - ((o['CALLS_LTP'].shift(-3)) * 2)
    call['CALLS 400 sprade'] = o['CALLS_LTP'] - ((o['CALLS_LTP'].shift(-4)) * 2)
    call['CALLS 500 sprade'] = o['CALLS_LTP'] - ((o['CALLS_LTP'].shift(-5)) * 2)
    call['CALLS 600 sprade'] = o['CALLS_LTP'] - ((o['CALLS_LTP'].shift(-6)) * 2)
    call = call[call.index > cmp].dropna().iloc[:12]
    put = pd.DataFrame()
    put['PUTS 100 sprade'] = o['PUTS_LTP'] - ((o['PUTS_LTP'].shift(1)) * 2)
    put['PUTS 200 sprade'] = o['PUTS_LTP'] - ((o['PUTS_LTP'].shift(2)) * 2)
    put['PUTS 300 sprade'] = o['PUTS_LTP'] - ((o['PUTS_LTP'].shift(3)) * 2)
    put['PUTS 400 sprade'] = o['PUTS_LTP'] - ((o['PUTS_LTP'].shift(4)) * 2)
    put['PUTS 500 sprade'] = o['PUTS_LTP'] - ((o['PUTS_LTP'].shift(5)) * 2)
    put['PUTS 600 sprade'] = o['PUTS_LTP'] - ((o['PUTS_LTP'].shift(6)) * 2)
    put = put[put.index < cmp].dropna().iloc[-12:]
    ratio = pd.concat([put, call])

    def color_range(val):
        color = 'red' if 0.5 <= val <= 8 else 'black'
        return f'color: {color}'

    ratio = ratio.style.applymap(color_range)
      
  else:
    
    call = pd.DataFrame()
    call['CALLS 50 sprade'] = o['CALLS_LTP'] - ((o['CALLS_LTP'].shift(-1)) * 2)
    call['CALLS 100 sprade'] = o['CALLS_LTP'] - ((o['CALLS_LTP'].shift(-2)) * 2)
    call['CALLS 150 sprade'] = o['CALLS_LTP'] - ((o['CALLS_LTP'].shift(-3)) * 2)
    call['CALLS 200 sprade'] = o['CALLS_LTP'] - ((o['CALLS_LTP'].shift(-4)) * 2)
    call['CALLS 250 sprade'] = o['CALLS_LTP'] - ((o['CALLS_LTP'].shift(-5)) * 2)
    call['CALLS 300 sprade'] = o['CALLS_LTP'] - ((o['CALLS_LTP'].shift(-6)) * 2)
    call = call[call.index > cmp].dropna().iloc[:12]
    put = pd.DataFrame()
    put['PUTS 50 sprade'] = o['PUTS_LTP'] - ((o['PUTS_LTP'].shift(1)) * 2)
    put['PUTS 100 sprade'] = o['PUTS_LTP'] - ((o['PUTS_LTP'].shift(2)) * 2)
    put['PUTS 150 sprade'] = o['PUTS_LTP'] - ((o['PUTS_LTP'].shift(3)) * 2)
    put['PUTS 200 sprade'] = o['PUTS_LTP'] - ((o['PUTS_LTP'].shift(4)) * 2)
    put['PUTS 250 sprade'] = o['PUTS_LTP'] - ((o['PUTS_LTP'].shift(5)) * 2)
    put['PUTS 300 sprade'] = o['PUTS_LTP'] - ((o['PUTS_LTP'].shift(6)) * 2)
    put = put[put.index < cmp].dropna().iloc[-12:]
    ratio = pd.concat([put, call])


    def color_range(val):
        color = 'red' if 0.5 <= val <= 8 else 'black'
        return f'color: {color}'


    ratio = ratio.style.applymap(color_range)
  with tab3:
      st.subheader('Ration Sprade strategy')
      st.text(f"Last Update : {last_update}")
      st.table(ratio)
  # creating importent futters
  st.write(index)
  col1, col2= st.columns(2) #,vertical_alignment='top'
  col1.metric('**Spot price**',cmp)
  
  pcr= np.round(o.PUTS_OI.sum()/o.CALLS_OI.sum(),2)
  col2.metric('**PCR:**',pcr)
  
 
except:
  st.text('Please select accurate expiry date')  


