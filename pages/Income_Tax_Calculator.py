# import all importent library
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

#configaration of page
st.set_page_config(
    page_title="sumancapz",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded")

# create titel of the page
st.title(":red-background[Income tax] :blue-background[Calculator]")


# creating tabs for different income
salary,house,business,capital,other,deduction=st.tabs(["Salary","House Property","Business Income" ,"Capital Gain","Others Income","Deduction u/s-80"])
# input forms of salary income
with salary:
    st.header("**Income** From :blue[Salary]", divider= True)
    basic_salary= st.number_input("Annual Basic salary",placeholder="Your 12 month total basic salary",format="%0.0f")
    d_a= st.number_input("D.A (Dearness Allowance)",placeholder="Dearnes allowances",format="%0.0f")
    h_r_a= st.number_input("H.R.A (House Rent Allowance)",placeholder="House Rent allowances",format="%0.0f")
    h_r_d= st.number_input("House rent Deduction U/s-10(13(A))",placeholder= "out of three condition lest amount allowed for deduction", help= "1. 50% or 60% of (basic+DA); \n 2. actual rent less 10% of (basic+DA); \n 3. actual rent received \n -- which ever is less",format="%0.0f")
    m_a= st.number_input("M.A (Medical Allowance)",placeholder="Medical allowances",format="%0.0f")
    other_allowances= st.number_input("Other allowances",format="%0.0f",placeholder="total of all other allowances")
    perquisites = st.number_input("total Perquisites (Extra benifits)",format="%0.0f",placeholder="any other benifits shown in u/s-17(2)", help="free accomodation, car or bus service etc...")
    st.subheader("Deduction u/s-16",divider= 'red')
    st.markdown("Standared Deduction u/s -16(i) has considered acording to tax rules", help="1. for New tax regim 75,0000 \n 2. for old tax regim 50,000")
    e_a= st.number_input("Entertainment Allowance u/s-16(ii)",format="%0.0f",placeholder="Deduction applicable only in old tax regim")
    p_tax= st.number_input("Profational tax u/s-16(iii)",format="%0.0f",placeholder="Deduction applicable only in old tax regim")
# input forms for Rental income
with house:
    st.header("**Income** From :blue[House Property]", divider= True)
    r_i= st.number_input("Annual Rental Income (excluding local tax)",format="%0.0f",placeholder="applicable only for let-out or deemed to be let-out property")
    st.subheader("Deduction u/s-24",divider= 'red')
    h_s_d= st.number_input("Standared deduction u/s-24(a) ",value=0,max_value= 30000,placeholder="applicable ony on let-out or deemed to be let-out property")
    int_d= st.number_input("Deduction on Interest on Loan u/s-24(b)",value=0, max_value=200000,placeholder= "annual interest payment on house building loan")
# input forms for Business or profational income
with business:
    st.header("Income from :blue[PGBP]",divider= True)
    pgbp= st.number_input("Profit or gain from Business or Profassion",format="%0.0f",placeholder= "Net profit on business or gain from profassion")
# input forms for Capital gain incmoe.. hear only financial assets has considered in calculation
with capital:
    st.header("Income from :blue[Capital gain]",divider= True)
    ltcg= st.number_input("total Long term capital gain",format="%0.0f",placeholder="gain from selling long term assets" )
    stcg= st.number_input("total short term capital gain",format="%0.0f",placeholder="gain from selling short term assets" )
    st.subheader("Deduction u/s-54",divider= 'red')
    cg_d= st.number_input("Deduction u/s 54, 54F, 54B, 54EC etc..", format="%0.0f",placeholder="Deduction for purchase new property or diposit into special scheme" )
# input forms for other source income
with other:
    st.header("Income from :blue[Other source]",divider= True)
    st.markdown("Taxable @ :red[slab rate]")
    sbi= st.number_input("saving bank Interest", format="%0.0f", placeholder="as per bank statment")
    fd= st.number_input("Fixed dipost Interest", format="%0.0f", placeholder="all realised and accural interest on dipost in bank or post office")
    div= st.number_input("Dividend Income", format="%0.0f", placeholder="all equity share dividend as per dividend statment by broker")
    o_in= st.number_input("any other income", format="%0.0f", placeholder="any other income chargable @ slab rate line- pension")
    st.markdown("Taxable @ :red[Special rate]")
    lotary= st.number_input("winning of Lotary or games or gambling",format="%0.0f", placeholder="even cripto trading income")
    spec_other= st.number_input("Others income (tax cargable at special rate)", format="%0.0f", placeholder="cripto currency or currency exchange incom")
# input forms for deduction spasified under 80
with deduction:
    st.header("Deduction u/s :blue[80]",divider= True)
    c= st.number_input("80C[PF,LIC,PPF,HBL principal,ELSS,ULIP,NSC etc.]", format="%0.0f")
    ccd=st.number_input("80CCD(1b): diposit into NPS",value=0,max_value= 50000)
    self_d= st.number_input("80D: Self", value=0, max_value= 25000,placeholder= "self, spouse and children insurance primium and expenses",help="up to 25,000/- for health insurance primium and 5,000/- for preventive checkup")
    parents_d= st.number_input("80D: Parents", value=0, max_value= 50000,placeholder= "parents insurance primium or heath expenses",help="up to age 60 maximm 25,000 on primium and 5,000 preventive checkup. for above 60 insurance or preventive care up to 50,000/-")
    tta=st.number_input("80TTA: Saving bank interest deduction", value=sbi, max_value= 10000,placeholder= "interest deduction applicable up to 10,000/- age below 60",help="1. 10,000 \n 2. actual saving bank interest \n which ever is less")
    g=st.number_input("80G : Donation",format="%0.0f",placeholder= "Deduction amout",help="for National Charitable trust 100% deduction allowd and other registered caritable trast 50% deduction allowed")
    o_d= st.number_input("Others deduction U/S-80",format="%0.0f",placeholder= "any other deduction allowed under any subsection of 80")  
# static data
#new tax rate 2024
first_new_slab= 0.05
second_new_slab= 0.10
third_new_slab= 0.15
fourth_new_slab= 0.20
fifth_new_slab= 0.25
sixth_new_slab= 0.30
new_tax_rebate_24= 20000
new_tax_rebate_25= 60000
# old tax rate
first_old_slab= 0.05
second_old_slab= 0.20
third_old_slab= 0.30
old_tax_rebate= 12500
CESS= 0.04
#special tax rate
ltcg_tax_rate= 0.125
stcg_tax_rate= 0.20
lottery_tax= 0.30

#total income under old tax
if basic_salary+d_a+(h_r_a-h_r_d)+m_a+other_allowances+ perquisites-50000-e_a- p_tax> 0:
    old_salary_income= basic_salary+d_a+(h_r_a-h_r_d)+m_a+other_allowances+ perquisites-50000-e_a- p_tax
else:
    old_salary_income= 0
house_income= r_i-h_s_d-int_d
other_income= sbi+ fd+ div + o_in
total_deduction= c+ ccd+self_d+parents_d + tta+ g+o_d
normal_old_income= old_salary_income+ house_income+other_income+pgbp-total_deduction
#total income under new tax 
if basic_salary+d_a+h_r_a+m_a+other_allowances+ perquisites-75000 >0:
    new_salary_income= basic_salary+d_a+h_r_a+m_a+other_allowances+ perquisites-75000
else:
    new_salary_income= 0
normal_new_income= new_salary_income+ r_i+other_income+pgbp
# special rate tax
ltcg_tax= np.ceil(((ltcg-cg_d)*ltcg_tax_rate)/10)*10  
stcg_tax=np.ceil((stcg*stcg_tax_rate)/10)*10
other_special_tax= np.ceil(((lotary+spec_other)*lottery_tax)/10)*10
# creating button to calculation of tax for the FY 2024-25 and AY 2025-2026
butt1, butt2= st.columns(2,gap='medium')
if butt1.button("Calculate for F.A 2024-25",type="primary"):
    # new tax calculation for FY 2024-2025
    if normal_new_income <= 300000:
        normal_new_tax=0
    elif normal_new_income <=700000:
        normal_new_tax= (normal_new_income - 300000) * first_new_slab
    elif normal_new_income <= 1000000:
        normal_new_tax= (normal_new_income - 700000) * second_new_slab + 400000 * first_new_slab
    elif normal_new_income <= 1200000:
        normal_new_tax= (normal_new_income - 1000000) * third_new_slab + 300000 * second_new_slab + 400000 * first_new_slab
    elif normal_new_income <= 1500000:
        normal_new_tax= (normal_new_income - 1200000) * fourth_new_slab + 200000 * third_new_slab + 300000 * second_new_slab + 400000 * first_new_slab
    else:
        normal_new_tax= (normal_new_income - 1500000) * sixth_new_slab + 300000 * fourth_new_slab + 200000 * third_new_slab + 300000 * second_new_slab + 400000 * first_new_slab
    # total tax under new tax regim
    basic_new_tax=np.ceil((normal_new_tax+ltcg_tax+ stcg_tax+other_special_tax)/10)*10
    # calculation of rebate under new tax
    if basic_new_tax <= new_tax_rebate_24:
        new_rebate= basic_new_tax
    else:
        new_rebate= 0
    new_income_tax= basic_new_tax- new_rebate
    new_cess= np.ceil(new_income_tax*CESS / 10) * 10
    new_total_tax= new_income_tax + new_cess
    # Old tax calculation
    if normal_old_income <= 250000:
        normal_old_tax=0
    elif normal_old_income <=500000:
        normal_old_tax= (normal_old_income - 250000) * first_old_slab
    elif normal_old_income <= 1000000:
        normal_old_tax= (normal_old_income - 500000) * second_old_slab + 250000 * first_old_slab
    else :
        normal_old_tax= (normal_old_income - 1000000) * third_old_slab + 500000 * second_old_slab + 250000 * first_old_slab
    # total taxable income under old tax regim
    basic_old_tax=np.ceil((normal_old_tax+ ltcg_tax+ stcg_tax+other_special_tax)/10)*10
    # calculation of rebate under old tax
    if basic_old_tax <= old_tax_rebate:
        old_rebate= basic_old_tax
    else:
        old_rebate= 0
    old_income_tax= basic_old_tax- old_rebate
    old_cess= np.ceil(old_income_tax*CESS / 10) * 10
    old_total_tax= old_income_tax + old_cess
    # Display the income summary 
    st.subheader(":blue[Summary] of income",divider="orange")
    col1,col2,col3= st.columns(3)
    col1.metric("Salary Income", str(new_salary_income))
    col2.metric("House property", str(house_income))
    col3.metric("Business income", str(pgbp))
    col1.metric("LTCG", str(ltcg-cg_d))
    col2.metric("STCG", str(stcg))
    col3.metric("Others Income", str(other_income+lotary+spec_other))
    col2.metric("Deduction", str(total_deduction))
    # display the bar chart
    try:
        fig, ax = plt.subplots()
        ax.pie([new_salary_income,r_i,pgbp,ltcg-cg_d+stcg,other_income+lotary+spec_other], labels=["Salary","House Property","Business Income" ,"Capital Gain","Others Income"], autopct='%1.1f%%')
        col3.pyplot(fig)
        
    except:
        pass
    # showing total tax liability under new tax regim
    left, right= st.columns(2)
    left.subheader(":blue[New Tax] Regim", divider="gray",anchor=False)
    con1=left.container(border=True)
    text, num= con1.columns([2, 1])
    text.markdown("Basic tax")
    num.markdown(f"{basic_new_tax}")
    text.markdown(":red[Less:] Tax Rebate(u/s-87A)")
    num.markdown(f"{new_rebate}")
    text.markdown("Income tax")
    num.markdown(f"{new_income_tax}")
    text.markdown(":blue[Add:] Education cess")
    num.markdown(f"{new_cess}")
    text.markdown("Total Tax")
    num.markdown(f"{new_total_tax}")

    # showing the total tax liability under old tax regim
    right.subheader(":orange[Old Tax] Regim", divider="gray",anchor=False)
    con2=right.container(border=True)
    text, num= con2.columns([2, 1])
    text.markdown("Basic tax")
    num.markdown(f"{basic_old_tax}")
    text.markdown(":red[Less:] Tax Rebate(u/s-87A)")
    num.markdown(f"{old_rebate}")
    text.markdown("Income tax")
    num.markdown(f"{old_income_tax}")
    text.markdown(":blue[Add:] Education cess")
    num.markdown(f"{old_cess}")
    text.markdown("Total Tax")
    num.markdown(f"{old_total_tax}")
    if new_total_tax> old_total_tax:
        st.subheader(f"If you select ***Old Tax regim*** you will get ₹ {new_total_tax-old_total_tax} tax benefit",anchor=False)
    elif new_total_tax< old_total_tax:
        st.subheader(f"If you select ***New Tax regim*** you will get ₹ {old_total_tax-new_total_tax} tax benefit",anchor=False)
# # creating button to calculation of tax for the FY 2025-26 and AY 2026-2027
if butt2.button("Calculate for F.A 2025-26",type="primary"):
    # new tax calculation for FY 2025-2026
    if normal_new_income <= 400000:
        normal_new_tax=0
    elif normal_new_income <=800000:
        normal_new_tax= (normal_new_income - 400000) * first_new_slab
    elif normal_new_income <= 1200000:
        normal_new_tax= (normal_new_income - 800000) * second_new_slab + 400000 * first_new_slab
    elif normal_new_income <= 1600000:
        normal_new_tax= (normal_new_income - 1200000) * third_new_slab + 400000 * second_new_slab + 400000 * first_new_slab
    elif normal_new_income <= 2000000:
        normal_new_tax= (normal_new_income - 1600000) * fourth_new_slab + 400000 * third_new_slab + 400000 * second_new_slab + 400000 * first_new_slab
    elif normal_new_income <= 2400000:
        normal_new_tax= (normal_new_income - 2000000) * fifth_new_slab + 400000 * fourth_new_slab + 400000 * third_new_slab + 400000 * second_new_slab + 400000 * first_new_slab
    else:
        normal_new_tax= (normal_new_income - 2400000) * sixth_new_slab + 400000 * fourth_new_slab + 400000 * third_new_slab + 400000 * second_new_slab + 400000 * first_new_slab
    # total tax under new tax regim
    basic_new_tax=np.ceil((normal_new_tax+ltcg_tax+ stcg_tax+other_special_tax)/10)*10
    # calculation of rebate under new tax
    if basic_new_tax <= new_tax_rebate_25:
        new_rebate= basic_new_tax
    else:
        new_rebate= 0
    new_income_tax= np.ceil((basic_new_tax- new_rebate)/10)*10
    new_cess= np.ceil(new_income_tax*CESS / 10) * 10
    new_total_tax= new_income_tax + new_cess
    # Old tax calculation
    if normal_old_income <= 250000:
        normal_old_tax=0
    elif normal_old_income <=500000:
        normal_old_tax= (normal_old_income - 250000) * first_old_slab
    elif normal_old_income <= 1000000:
        normal_old_tax= (normal_old_income - 500000) * second_old_slab + 250000 * first_old_slab
    else :
        normal_old_tax= (normal_old_income - 1000000) * third_old_slab + 500000 * second_old_slab + 250000 * first_old_slab
    # total taxable income under old tax regim
    basic_old_tax=np.ceil((normal_old_tax+ ltcg_tax+ stcg_tax+other_special_tax)/10)*10
    # calculation of rebate under old tax
    if basic_old_tax <= old_tax_rebate:
        old_rebate= basic_old_tax
    else:
        old_rebate= 0
    old_income_tax=np.ceil((basic_old_tax- old_rebate)/10)*10
    old_cess= np.ceil(old_income_tax*CESS / 10) * 10
    old_total_tax= old_income_tax + old_cess
    # display the income summary 
    st.subheader(":blue[Summary] of income",divider="orange")
    col1,col2,col3= st.columns(3)
    col1.metric("Salary Income", str(new_salary_income))
    col2.metric("House property", str(house_income))
    col3.metric("Business income", str(pgbp))
    col1.metric("LTCG", str(ltcg-cg_d))
    col2.metric("STCG", str(stcg))
    col3.metric("Others Income", str(other_income+lotary+spec_other))
    col2.metric("Deduction", str(total_deduction))
    # showing different income bar chart
    try:
        fig, ax = plt.subplots()
        ax.pie([new_salary_income,r_i,pgbp,ltcg-cg_d+stcg,other_income+lotary+spec_other], labels=["Salary","House Property","Business Income" ,"Capital Gain","Others Income"], autopct='%1.1f%%')
        col3.pyplot(fig)
        
    except:
        pass
    # showing income tax under new regim
    left, right= st.columns(2)
    left.subheader(":blue[New Tax] Regim", divider="gray",anchor=False)
    con1=left.container(border=True)
    text, num= con1.columns([2, 1])
    text.markdown("Basic tax")
    num.markdown(f"{basic_new_tax}")
    text.markdown(":red[Less:] Tax Rebate(u/s-87A)")
    num.markdown(f"{new_rebate}")
    text.markdown("Income tax")
    num.markdown(f"{new_income_tax}")
    text.markdown(":blue[Add:] Education cess")
    num.markdown(f"{new_cess}")
    text.markdown("Total Tax")
    num.markdown(f"{new_total_tax}")

    # showing tax liability under old tax regim
    right.subheader(":orange[Old Tax] Regim", divider="gray",anchor=False)
    con2=right.container(border=True)
    text, num= con2.columns([2, 1])
    text.markdown("Basic tax")
    num.markdown(f"{basic_old_tax}")
    text.markdown(":red[Less:] Tax Rebate(u/s-87A)")
    num.markdown(f"{old_rebate}")
    text.markdown("Income tax")
    num.markdown(f"{old_income_tax}")
    text.markdown(":blue[Add:] Education cess")
    num.markdown(f"{old_cess}")
    text.markdown("Total Tax")
    num.markdown(f"{old_total_tax}")
    if new_total_tax> old_total_tax:
        st.subheader(f"If you select **Old Tax regim** you will get ₹ {new_total_tax-old_total_tax} tax benefit.",anchor=False)
    elif new_total_tax< old_total_tax:
        st.subheader(f"If you select ***New Tax regim*** you will get ₹ {old_total_tax-new_total_tax} tax benefit.",anchor=False)
