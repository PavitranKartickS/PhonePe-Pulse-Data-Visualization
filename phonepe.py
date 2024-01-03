#Libraries for use
import os
import json
import pandas as pd
import numpy as np
import json
import mysql.connector 
import sqlalchemy
from sqlalchemy import create_engine
import plotly.express as px
from urllib.request import urlopen
from streamlit_option_menu import option_menu
import geopandas as gpd
import streamlit as st
from PIL import Image


#Streamlit Page Set up
icon = Image.open("Icon.png")
st.set_page_config(page_title="Phonepe Pulse Data Analysis and Visualization   |   S.Pavitran Kartick",
                page_icon= icon,
                layout="wide",
                initial_sidebar_state= "expanded",
                )
st.sidebar.header("📊💸📊💸📊💸📊💸📊 :white[**Greetings! Welcome to the dashboard**]  📊💸📊💸📊💸📊💸📊")

#Connecting to MYSQL Workbench
mydb =  mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "12345",
    database = "phonepe"

)
mycursor = mydb.cursor()

#Option Menu for the Side bar:

with st.sidebar:
    selected = option_menu("Main Menu",['Home','Top Charts','Explore Data','About'],
                        icons=["house","graph-up-arrow","bar-chart-line", "exclamation-circle"],
                        menu_icon= "menu-button-wide",
                        default_index=0,
                        styles={"nav-link": {"font-size": "14px", "text-align": "justified", "margin": "-1px", "--hover-color": "#Db65bc"},
                                "nav-link-selected": {"background-color": "#9650aa"}})
    

st.sidebar.markdown("The dashboard application is brought to you by **S.Pavitran Kartick**") 
st.sidebar.markdown("Data for this Project has been cloned from Phonepe Pulse Github Repository")


#HOME
if selected == "Home":
    st.markdown("# :orange[PhonePe-Pulse Data Analysis and Visualization]🔬")
    st.markdown("## :orange[A User-Friendly App Using Plotly and Streamlit]")
    col1,col2 = st.columns([4,1],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :red[Technologies used :] Github Cloning, Python, Pandas, MySQL, SQLAlchemy,GeoPandas,Numpy, Streamlit, and Plotly.")
        st.markdown("### :red[Domain :] Fintech")
        st.markdown("### :red[Synopsis :] With this web application, we can perform several types of analysis on the phonepe pulse data and deduce useful insights on overall User transactions, number of registered users, top users sorted by states, districts, brands. Types of data visualization include bar charts, pie charts, geo map visualization.")
                                            
    with col2:
        st.image("home.png")

#TOP CHARTS
if selected == "Top Charts":
    st.markdown("## :red[Top Charts]")
    Type = st.selectbox("**Type**", ("Transactions", "Users"))
    column1,column2= st.columns([1,2],gap="medium")
    with column1:
        Year = st.slider("**Year**", min_value=2018, max_value=2023)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)

    with column2:
        st.info(
                """
                #### Page Insights :
                - Overall statistics of the states on a particular Year and Quarter.
                - Top 10 States and Districts based on the Total transactions and Total amount spent through phonepe.
                - Top 10 States and Districts based on the Total phonepe users and their app opening frequency.
                - Top 10 mobile brands and its percentage based on the how many people use phonepe.
                """,icon="💡"
                )
        
#TOP CHARTS - TRANSACTIONS
    if Type == "Transactions":
        col1,col2 = st.columns([1,1],gap="large")
        
        with col1:
            if Year == 2023 and Quarter in [4]:
                st.markdown("#### Sorry, No Data to Display for 2023 in quarter 4")
            st.markdown("### :red[State]")
            mycursor.execute(f"select States, sum(Trans_count) as Total_Transaction_Count, sum(Trans_amount) as Total from aggregated_transaction where Years = {Year} and Quarter = {Quarter} group by States order by Total desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns = ['States','Transactions_Count','Total_Amount'])
            fig = px.pie(df, values = 'Total_Amount',
                            names = 'States',
                            title = 'Top 10 States',
                            color_discrete_sequence = px.colors.sequential.Aggrnyl,
                            hover_data=['Transactions_Count'],
                            labels={'Transactions_Count':'Transactions_Count'})
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
            
        with col2:
            if Year == 2023 and Quarter in [4]:
                st.markdown("#### Sorry No Data to Display for 2023 in quarter 4")
            st.markdown("### :red[District]")
            mycursor.execute(f"select District_name, sum(District_count) as Total_Count, sum(District_amount) as Total from map_transaction where Years ={Year} and Quarter = {Quarter} group by District_name order by Total desc limit 10")
            df =  pd.DataFrame(mycursor.fetchall(),columns=['District','Transactions_Count','Total_Amount'])

            fig = px.pie(df,values="Total_Amount",
                        names= 'District',
                        title='Top 10 Districts',
                        color_discrete_sequence=px.colors.sequential.Aggrnyl,
                        hover_data=['Transactions_Count'],
                        labels={'Transactions_Count':'Transactions_Count'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)

#TOP CHARTS - USERS
    if Type == "Users":
        col1,col2,col3 = st.columns([2,2,2],gap="medium")
        
        with col1:
            st.markdown("### :red[Brands]")
            if Year == 2023 and Quarter in [4]:
                st.markdown("#### Sorry No Data to Display for 2023 in quarter 4")
            else:
                mycursor.execute(f"select Brands, sum(User_count) as Total_Count, avg(Percentage)*100 as Avg_Percentage from aggregated_user where Years={Year} and Quarter={Quarter} group by Brands order by Total_Count desc limit 10")
                df=pd.DataFrame(mycursor.fetchall(),columns=['Brand','Total_Users','Avg_Percentage'])
                fig = px.bar(df,
                            title='Top 10 Brands',
                            x="Total_Users",
                            y="Brand",
                            orientation='h',
                            color='Avg_Percentage',
                            color_continuous_scale=px.colors.sequential.Aggrnyl)
                st.plotly_chart(fig,use_container_width=True)   
    
        with col2:
            st.markdown("### :red[District]")
            if Year == 2023 and Quarter in [4]:
                st.markdown("#### Sorry No Data to Display for 2023 in quarter 4")
            mycursor.execute(f"select District_name, sum(User_count) as Total_Users, sum(Open_count) as Total_App_Opens from map_user where Years={Year} and Quarter={Quarter} group by District_name order by Total_Users desc limit 10")
            df=pd.DataFrame(mycursor.fetchall(),columns=['District', 'Total_Users','Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(float)
            fig = px.bar(df,
                            title='Top 10 Districts',
                            x="Total_Users",
                            y="District",
                            orientation='h',
                            color='Total_Users',
                            color_continuous_scale=px.colors.sequential.Aggrnyl)
            st.plotly_chart(fig,use_container_width=True)
                        
        with col3:
            if Year == 2023 and Quarter in [4]:
                st.markdown("#### Sorry No Data to Display for 2023 in quarter 4")
            st.markdown("### :red[State]")
            mycursor.execute(f"select States, sum(User_count) as Total_Users, sum(Open_count) as Total_App_Opens from map_user where Years={Year} and Quarter={Quarter} group by States order by Total_Users desc limit 10")
            df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
            fig = px.pie(df, values='Total_Users',
                                names='State',
                                title='Top 10 States',
                                color_discrete_sequence=px.colors.sequential.Aggrnyl,
                                hover_data=['Total_Appopens'],
                                labels={'Total_Appopens':'Total_Appopens'})

            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig,use_container_width=True)
    
# EXPLORE DATA
if selected == "Explore Data":
    Year = st.slider("**Year**", min_value=2018, max_value=2023)
    Quarter = st.slider("Quarter", min_value=1, max_value=4)
    Type = st.selectbox("**Type**", ("Transactions", "Users"))
    col1,col2 = st.columns(2)
                        
# Explore data - TRANSACTIONS
    if Type == "Transactions":

        # Overall State data -  TRANSACTION AMOUNT INDIA MAP
        with col1:
            st.markdown("## :red[Overall State Data - Transactions Amount]")
            url = 'https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson'
            with urlopen(url) as response:
                state_lines = json.load(response)


            mycursor.execute(f"select States, sum(District_count) as Total_Transactions, sum(District_amount) as Total_amount from map_transaction where Years={Year} and Quarter={Quarter} group by States order by States")
            df1=pd.DataFrame(mycursor.fetchall(),columns=['State','Total_Transactions','Total_amount'])
            sta_list = ['Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                        'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                        'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa', 'Gujarat',
                        'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir', 'Jharkhand',
                        'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 'Madhya Pradesh',
                        'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland',
                        'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim',
                        'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                        'Uttarakhand', 'West Bengal']
            df2=pd.Series(data=sta_list, name="State")
            df1['State']=df2

            fig = px.choropleth(df1,
                                geojson=state_lines,
                                featureidkey='properties.ST_NM',
                                locations='State',
                                color='Total_amount',
                                color_continuous_scale='ylorbr')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
        
        # Overall State Data - TRANSACTIONS COUNT - INDIA MAP
        with col2:
            st.markdown("## :red[Overall State Data - Transactions Count]")


            mycursor.execute(f"select States, sum(District_count) as Total_Transactions, sum(District_amount) as Total_amount from map_transaction where Years={Year} and Quarter={Quarter} group by States order by States")
            df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
            sta_list = ['Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                        'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                        'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa', 'Gujarat',
                        'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir', 'Jharkhand',
                        'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 'Madhya Pradesh',
                        'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland',
                        'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim',
                        'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                        'Uttarakhand', 'West Bengal']
            df2=pd.Series(data=sta_list, name="State")
            df1.Total_Transactions = df1.Total_Transactions.astype(int)
            df1['State']=df2

            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                                featureidkey='properties.ST_NM',
                                locations='State',
                                color='Total_Transactions',
                                color_continuous_scale='ylorbr')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
    
        
        # BAR CHART - TOP PAYMENT TYPE
        st.markdown("## :red[Top Payment Type]")
        mycursor.execute(f"select Trans_name, sum(Trans_count) as Total_Transactions, sum(Trans_amount) as Total_amount from aggregated_transaction where Years={Year} and Quarter={Quarter} group by Trans_name order by Trans_name")
        df = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_type', 'Total_Transactions','Total_amount'])

        fig = px.bar(df,
                    title='Transaction Types vs Total_Transactions',
                    x="Transaction_type",
                    y="Total_Transactions",
                    orientation='v',
                    color='Total_amount',
                    color_continuous_scale=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig,use_container_width=False)

        # BAR CHART TRANSACTIONS - DISTRICT WISE DATA
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :red[Select any State to explore more]")
        selected_state = st.selectbox("",
                            ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                            'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                            'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                            'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                            'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                            'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)

        mycursor.execute(f"select States,District_name,Years,Quarter, sum(District_count) as Total_Transactions, sum(District_amount) as Total_amount from map_transaction where Years={Year} and Quarter={Quarter} and States ='{selected_state}'group by States,District_name,Years,Quarter order by States,District_name")

        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State','District','Year','Quarter',
                                                                'Total_Transactions','Total_amount'])
        fig = px.bar(df1,
                    title=selected_state,
                    x="District",
                    y="Total_Transactions",
                    orientation='v',
                    color='Total_amount',
                    color_continuous_scale=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig,use_container_width=True)
    
# EXPLORE DATA - USERS      
    if Type == "Users":
        # Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :red[Overall State Data - User App opening frequency]")
        mycursor.execute(f"select States, sum(User_count) as Total_Users, sum(Open_count) as Total_Appopens from map_user where Years={Year} and Quarter={Quarter} group by States order by States")
        df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
        sta_list = ['Andaman & Nicobar', 'Andhra Pradesh', 'Arunachal Pradesh',
                    'Assam', 'Bihar', 'Chandigarh', 'Chhattisgarh',
                    'Dadra and Nagar Haveli and Daman and Diu', 'Delhi', 'Goa', 'Gujarat',
                    'Haryana', 'Himachal Pradesh', 'Jammu & Kashmir', 'Jharkhand',
                    'Karnataka', 'Kerala', 'Ladakh', 'Lakshadweep', 'Madhya Pradesh',
                    'Maharashtra', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland',
                    'Odisha', 'Puducherry', 'Punjab', 'Rajasthan', 'Sikkim',
                    'Tamil Nadu', 'Telangana', 'Tripura', 'Uttar Pradesh',
                    'Uttarakhand', 'West Bengal']
        df2=pd.Series(data=sta_list, name="State")
        df1.Total_Appopens = df1.Total_Appopens.astype(float)
        df1['State']=df2



        fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',
                        locations='State',
                        color='Total_Appopens',
                        color_continuous_scale='ylorbr')

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True)

        # BAR CHART TOTAL UERS - DISTRICT WISE DATA 
        st.markdown("## :red[Select any State to explore more]")
        selected_state = st.selectbox("",
                            ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                            'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                            'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                            'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                            'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                            'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)

        mycursor.execute(f"select States,Years,Quarter,District_name, sum(User_count) as Total_Users, sum(Open_count) as Total_Appopens from map_user where Years={Year} and Quarter={Quarter} and States='{selected_state}' group by States, District_name, Years, Quarter order by States, District_Name")
        df=pd.DataFrame(mycursor.fetchall(), columns=['State','year', 'quarter', 'District', 'Total_Users','Total_Appopens'])
        df.Total_Users = df.Total_Users.astype(int)

        fig = px.bar(df,
                        title=selected_state,
                        x="District",
                        y="Total_Users",
                        orientation='v',
                        color='Total_Users',
                        color_continuous_scale=px.colors.sequential.Aggrnyl)
        st.plotly_chart(fig,use_container_width=True)

# MENU 4 - ABOUT
if selected == "About":
    col1,col2 = st.columns([3,3],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :red[About PhonePe Pulse:] ")
        st.write("##### India’s digital payments landscape has transformed dramatically and is expected to become a US$10 trillion opportunity in the next few years. PhonePe Pulse, India’s first interactive geospatial platform on digital payments, brings forth a series of initiatives including in-depth reports, insights and conversations showcasing the industry’s beat of progress!")
        
        st.write("##### Pulse is a notel interactive platform that is India's go-to destination for accurate and comprehensive data on digital payment trends. The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. The report is available as a free download on the PhonePe Pulse website and GitHub.")
        
        st.markdown("### :red[About PhonePe:] ")
        st.write("##### Founded in December 2015, PhonePe has become a homegrown success story, with its meteoric growth powered by India’s emerging digital ecosystem, particularly in the Unified Payments Interface (UPI) space. The company builds products and offerings tailored for the Indian market and has emerged as India’s largest payments app, enabling digital inclusion for consumers and merchants alike. With 380 million registered users, one in four Indians are now on PhonePe. The company has also successfully digitized over 30 million offline merchants spread across Tier 2,3,4 and beyond, covering 99% pin codes in the country. PhonePe is proud to help lead India’s country-wide digitization efforts and believes that this powerful public-private collaboration has made the Indian digital ecosystem a global exemplar.")
        
        st.write("**:red[My Project GitHub link]** ⬇️")
        st.write("https://github.com/PavitranKartickS/PhonePe-Pulse-Data-Visualization.git")

        
    with col2:
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.image("Pulseimg.png")




                               

