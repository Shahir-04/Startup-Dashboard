import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go
st.set_page_config(layout='wide',page_title='Startup Analysis')
df=pd.read_csv('Final_startup_data.csv')
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
    temp_df['axis_x']=temp_df['month'].astype('str')+'-'+temp_df['year'].astype('str')
    trace1=go.Line(x=temp_df['axis_x'],y=temp_df['amount'])
    data=[trace1]
    layout=go.Layout(title='')
    fig=go.Figure(data,layout)
    st.plotly_chart(fig)


def load_investor(investor):
    st.title(investor)
    load_df=df[df['Investors Name'].str.contains(investor)].sort_values('Date',ascending=False).head()[['Date','Startup Name','Industry Vertical','City','Investors Name','Investment Type','amount']]
    st.subheader('Most Recent Investment')
    st.dataframe(load_df)
    col1,col2=st.columns(2)   
    with col1:
        st.subheader('Biggest Investment(in Cr)')
        big_series=df[df['Investors Name'].str.contains(investor)].groupby('Startup Name')['amount'].sum().sort_values(ascending=False).head()
        trace1=go.Bar(x=big_series.index,y=big_series.values,hovertext=big_series.values)
        layout=go.Layout(title='')
        data=[trace1]
        fig=go.Figure(data,layout)
        st.plotly_chart(fig)

        st.subheader('Top Cities where startup is')
        cites_series=df[df['Investors Name'].str.contains(investor)].groupby('City')['amount'].sum().head()
        trace1=go.Pie(labels=cites_series.index,values=cites_series.values)
        layout=go.Layout(title='')
        data=[trace1]
        fig=go.Figure(data,layout)
        st.plotly_chart(fig)

    with col2:
        st.subheader('Sector Invested in')
        vertical_series=df[df['Investors Name'].str.contains(investor)].groupby('Industry Vertical')['amount'].sum().head()
        trace1=go.Pie(labels=vertical_series.index,values=vertical_series.values)
        data=[trace1]
        layout=go.Layout(title='')
        fig=go.Figure(data,layout)
        st.plotly_chart(fig)

        st.subheader('Stages')
        stage_series=df[df['Investors Name'].str.contains(investor)].groupby('Investment Type')['amount'].sum().head()
        trace1=go.Pie(labels=stage_series.index,values=stage_series.values)
        data=[trace1]
        layout=go.Layout(title='')
        fig=go.Figure(data,layout)
        st.plotly_chart(fig)
    
    st.subheader('Year on year investment')
    investment_series=df[df['Investors Name'].str.contains(investor)].groupby('year')['amount'].sum()
    trace1=go.Line(x=investment_series.index,y=investment_series.values)
    data=[trace1]
    layout=go.Layout(title='')
    fig=go.Figure(data,layout)
    st.plotly_chart(fig)

def load_startup(startup):
    st.title(startup)
    st.subheader('Recent Investment')
    sup=df[df['Startup Name']==startup][['Date','Startup Name','Industry Vertical','City','Investors Name','Investment Type','amount']].tail()
    st.dataframe(sup)
    col1,col2=st.columns(2)
    st.subheader('Top Investers')
    invester_name=df[df['Startup Name']==startup].groupby('Investors Name')['amount'].sum().sort_values(ascending=False).head()
    trace1=go.Pie(labels=invester_name.index,values=invester_name.values)
    data=[trace1]
    layout=go.Layout(title='')
    fig=go.Figure(data,layout)
    st.plotly_chart(fig)

    st.subheader('Investments')
    big_inverst=df[df['Startup Name']==startup].groupby('Date')['amount'].max().sort_values(ascending=False).head()
    trace1=go.Line(x=big_inverst.index,y=big_inverst.values)
    data=[trace1]
    layout=go.Layout(title='')
    fig=go.Figure(data,layout)
    fig.update_layout(autosize=True)
    st.plotly_chart(fig)

    test=list(df[df['Startup Name']==startup]['Industry Vertical'].values)
    check=df[df['Industry Vertical'].isin(test)].groupby('Startup Name')['Industry Vertical'].value_counts().sort_values(ascending=False).head()
    similar_startup=check.reset_index()['Startup Name']
    if len(test)>1:
        st.subheader('Similar Startups')
        with st.expander('Similar Startups'):
            st.dataframe(similar_startup)
    else:
        st.subheader('Similar Startups')
        st.write('There is no similar startup')
    
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
    startup_selecter=st.sidebar.selectbox('Select Startup',df['Startup Name'].unique().tolist())
    # st.title('Startup Analysis')
    b2=st.sidebar.button('Get Details')
    if b2:
        load_startup(startup_selecter)
    


