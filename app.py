#---------------Import Packages---------------#
import streamlit as st 
from faker import Faker
import random
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu

#---------------Page Setup---------------#
st.set_page_config(page_title="Podcast KPI Dashboard", page_icon="🎙️", layout="wide", initial_sidebar_state="expanded")
sidebar = st.sidebar


#---------------Import CSS---------------#
# open/create css object
with open('css/styles.css') as f:
    css = f.read()
#apply css to page
st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)



#---------------Create Data---------------#
# Initialize Faker
fake = Faker()

# Generate fake data for a date range
def generate_data(start_date, end_date):
    num_days = (end_date - start_date).days + 1  # Number of days in the date range
    daily_average = 37500  # Average listen time per day
    listeners_range = (25000, 35000)  # Range for listeners
    weekday_range = (40000, 55000)  # Range for weekdays
    weekend_range = (30000, 35000)  # Range for weekends
    
    # Generate data for each day in the date range
    data = {
        'date': [],
        'listen_time': [],
        'listeners': [],
        'listen_time_last_year': [],
        'listeners_last_year': []
    }
    
    # Generate data for each day
    for i in range(num_days):
        current_date = start_date + pd.Timedelta(days=i)
        date_str = current_date.strftime('%Y-%m-%d')
        
        # Generate data for the current year
        if current_date.dayofweek < 5:  # Monday to Friday
            listen_time = random.randint(*weekday_range)
        else:
            listen_time = random.randint(*weekend_range)
        listeners = random.randint(*listeners_range)
        
        # Generate data for the previous year
        prev_year_date = current_date - pd.DateOffset(years=1)
        prev_year_listen_time = random.randint(*weekday_range if prev_year_date.dayofweek < 5 else weekend_range)
        prev_year_listeners = random.randint(*listeners_range)
        
        data['date'].append(date_str)
        data['listen_time'].append(listen_time)
        data['listeners'].append(listeners)
        data['listen_time_last_year'].append(prev_year_listen_time)
        data['listeners_last_year'].append(prev_year_listeners)
    
    return pd.DataFrame(data)


#---------------App Build---------------#
_, col1, col2 = st.columns([2, .5, .25])
col1.markdown("*Click for more info 👉*")
with col2.popover("ℹ️"):
    st.subheader("👉Overview")
    st.markdown("""*This dashboard is designed to provide a high-level overview of the key metrics for our podcast.*""")
    st.write(" ")
    st.subheader("📍Data Sources")
    st.markdown("""The data is randomly created data to protect the privacy of the company this was built for.""")
    st.write(" ")
    st.subheader("📍Definitions")
    st.markdown("""**Listen Time:** The total number of minutes that users have listened to the podcast.""")
    st.markdown("""**Listeners:** The total number of verified listeners who have listened to the podcast. This means apple and spotify verified their devices.""")
    st.markdown("""**Downloads:** The total number of downloads of the podcast episodes.""")
#---------------Title---------------#
st.markdown(
    """
    <div class="title-container">
        <h1 class="title-text">Podcast KPI Dashboard</h1>
    </div>
    """,
    unsafe_allow_html=True
)


sidebar.write(" ")
sidebar.subheader("Filters", divider="gray")

#date items
#data is delayed by one day due to apple reporting
current_date = pd.Timestamp.today().date() - pd.Timedelta(days=1)
#start date is defaulted to 30 days prior to current date
start_date = current_date - pd.Timedelta(days=30)

_, _, col3 = st.columns([1, 1, .5])
#create date selector that overrides default values
date_range = sidebar.date_input('Select Date Range👇', value=[start_date, current_date])
if len(date_range) != 2:
    st.stop()
    
start_date, end_date = date_range


# Convert start_date and end_date to datetime objects if they're not already
start_date, end_date = pd.to_datetime(start_date), pd.to_datetime(end_date)



df = generate_data(start_date, end_date)
df["downloads"] = df["listeners"] * 3.5


st.header("Performance Overview", divider='blue')

#---------------Main Metrics---------------#

current_listen_time = df['listen_time'].sum()
current_listeners = df['listeners'].sum()
current_downloads = round(df['downloads'].sum(),0)

listeners_diff = random.randint(0, 10)
listen_time_diff = random.randint(0, 10)
downloads_diff = random.randint(5, 13)

st.subheader("Main Metrics", divider='gray')


with st.container(border=True):
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Listen Time", f"{current_listen_time:,}", f"↑ {listen_time_diff:.0f}%")
    col2.metric("Total Listeners", f"{current_listeners:,}", f"↑ {listeners_diff:.0f}%")
    col3.metric("Total Downloads", f"{current_downloads:,}", f"↑ {downloads_diff:.0f}%")
    
st.header("")
#---------------Graphs---------------#
st.subheader("Visual Breakdown", divider='gray')
fig_df = df.sort_values('date')



@st.experimental_fragment
def fragment():
    selected = option_menu(
        None,
        ["Listen Time", "Listeners", "Downloads"],
        icons=["headphones", "person-check", "download"],
        menu_icon="cast",
        default_index=0,
        orientation="horizontal",
        styles={
            "nav-link-selected": {"background-color":"#409cf4"}
            }
    )

    with st.container(border=True):
        if selected == "Listen Time":
            fig = px.line(fig_df, x='date', y='listen_time', title="Listen Time") #line chart
            
        elif selected == "Listeners":
            fig = px.line(fig_df, x='date', y='listeners', title="Listeners") #line chart
            
        elif selected == "Downloads":
            fig = px.line(fig_df, x='date', y='downloads', title="Downloads") #line chart
            
        st.plotly_chart(fig, use_container_width=True)
        
fragment()