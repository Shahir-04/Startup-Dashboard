import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
st.set_page_config(layout='wide',page_title='Startup Analysis')
df=pd.read_csv('C:/Users/shahi/OneDrive/Desktop/Seminar/dashboard_stremlit/cleaned_startup.csv')
df['Date']=pd.to_datetime(df['Date'],dayfirst=True,errors='coerce')
df['month']=df['Date'].dt.month
df['year']=df['Date'].dt.year

def load_overall_analysis():
    st.title('OverAll Analysis')
    col1,col2,col3,col4=st.columns(4)
    with col1:
        total=round(df['amount'].sum())
        st.metric('Total Amount',str(total)+" Cr")
    with col2:
        max1=df.groupby('Startup Name')['amount'].max().sort_values(ascending=False).head(1).values[0]
        st.metric('Maximum Amount',max1)
    with col3:
        avg=round(df.groupby('Startup Name')['amount'].sum().mean(),2)
        st.metric('Average Amount',avg)
    with col4:
        no_startup=df['Startup Name'].nunique()
        st.metric('Number of Startups',no_startup)
    st.header('Month on Month Analysis')
    sel=st.selectbox('Select',['Total','Count'])
    if sel=='Total':
        temp_df=df.groupby(['year','month'])['amount'].sum().reset_index()
    else:
        temp_df=df.groupby(['year','month'])['amount'].count().reset_index()
    temp_df['axis_X']=temp_df['month'].astype('str')+'-'+temp_df['year'].astype('str')
    fig,ax=plt.subplots()
    ax.plot(temp_df['axis_X'],temp_df['amount'])
    st.pyplot(fig)


def load_investor(investor):
    st.title(investor)
    load_df=df[df['Investors Name'].str.contains('Sequoia Capital India')].sort_values('Date',ascending=False).head()[['Date','Startup Name','Industry Vertical','City','Investors Name','Investment Type','amount']]
    st.subheader('Most Recent Investment')
    st.dataframe(load_df)
    col1,col2=st.columns(2)   
    with col1:
        st.subheader('Biggest Investment(in Cr)')
        big_series=df[df['Investors Name'].str.contains(investor)].groupby('Startup Name')['amount'].sum().sort_values(ascending=False).head()
        fig, ax=plt.subplots()
        ax.bar(big_series.index,big_series.values)
        st.pyplot(fig)

        st.subheader('Top Cities where startup is:')
        cites_series=df[df['Investors Name'].str.contains(investor)].groupby('City')['amount'].sum().head()
        fig1, ax1=plt.subplots()
        ax1.pie(cites_series.values,labels=cites_series.index)
        st.pyplot(fig1)

    with col2:
        st.subheader('Sector Invested in')
        vertical_series=df[df['Investors Name'].str.contains(investor)].groupby('Industry Vertical')['amount'].sum().head()
        fig, ax=plt.subplots()
        ax.pie(vertical_series.values,labels=vertical_series.index)
        st.pyplot(fig)
        st.subheader(" ")
        st.subheader('Stages')
        stage_series=df[df['Investors Name'].str.contains(investor)].groupby('Investment Type')['amount'].sum().head()
        fig1, ax1=plt.subplots()
        ax1.pie(stage_series.values,labels=stage_series.index)
        st.pyplot(fig1)
    
    st.subheader('Year on year investment')
    investment_series=df[df['Investors Name'].str.contains(investor)].groupby('year')['amount'].sum()
    fig2, ax2=plt.subplots()
    ax2.plot(investment_series.index,investment_series.values)
    st.pyplot(fig2)
st.sidebar.title('Startup Funding Analysis')
select=st.sidebar.selectbox('Select one',['Overall Analysis','Invester Name','Startup Name'])
if select=='Overall Analysis':
    load_overall_analysis()
elif select=='Invester Name':
    # st.title('Investor Analysis')
    selected_investor=st.sidebar.selectbox('Select Invester',sorted(set(df['Investors Name'].str.split(',').sum())))
    b1=st.sidebar.button('Get Details')
    if b1:
        load_investor(selected_investor)

else:
    st.sidebar.selectbox('Select Startup',df['Startup Name'].unique().tolist())
    # st.title('Startup Analysis')
    b2=st.sidebar.button('Get Details')
    


