import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
sns.set(style='dark')

def create_registered_seasonal_rental(df):
    registered_season_df = df.groupby('season')['registered'].sum().reset_index()
    return registered_season_df

def create_casual_seasonal_rental(df):
    casual_season_df = df.groupby('season')['casual'].sum().reset_index()
    return casual_season_df

def create_year_rental(df):
    year_df = df.groupby('yr')['cnt'].sum().reset_index()
    return year_df

df = pd.read_csv("../data/day.csv")
datetime_columns = ["dteday"]
for column in datetime_columns:
    df[column] = pd.to_datetime(df[column])

min_date = df["dteday"].min()
max_date = df["dteday"].max()

with st.sidebar:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("https://raw.githubusercontent.com/sorayasab/new-repo/master/bicycle.png", width=150)

    
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = df[(df["dteday"] >= str(start_date)) & 
                (df["dteday"] <= str(end_date))]

season_casual_df = create_casual_seasonal_rental(main_df)
season_registered_df = create_registered_seasonal_rental(main_df)
year_df = create_year_rental(main_df)

st.header('Bike Sharing Dashboard :sparkles:')

st.subheader('Total Bike Rentals per Season')

season_names = {1: 'Winter', 2: 'Spring', 3: 'Summer', 4: 'Fall'}
bar_width = 0.35
r1 = np.arange(len(season_registered_df))
r2 = [x + bar_width for x in r1]

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(r1, season_registered_df['registered'], color='skyblue', width=bar_width, label='Registered')
ax.bar(r2, season_casual_df['casual'], color='orange', width=bar_width, label='Casual')

ax.set_title('Total Bike Rentals per Season')
ax.set_xlabel('Season')
ax.set_ylabel('Total Rentals')
ax.set_xticks([r + bar_width/2 for r in range(len(season_registered_df))])
ax.set_xticklabels([season_names[season] for season in season_registered_df['season']])
ax.legend()

st.pyplot(fig)

st.subheader('Total Bike Rentals per Year')

fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(year_df['yr'].astype(str), year_df['cnt'], color='skyblue')

ax.set_title('Total Bike Rentals per Year')
ax.set_xlabel('Year')
ax.set_ylabel('Total Rentals')
ax.set_xticks(year_df['yr'])
ax.set_xticklabels(['2011' if year == 0 else '2012' for year in year_df['yr']])

st.pyplot(fig)
 

