import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set(style='dark')

# Function to get total count by hour
def get_total_count_by_hour_df(hour_df):
    hour_count_df = hour_df.groupby(by="hr").agg({"count_cr": ["sum"]})
    return hour_count_df

# Function to filter data by day
def count_by_day_df(day_df):
    day_df_count_2011 = day_df.query('dteday >= "2011-01-01" and dteday < "2012-12-31"')
    return day_df_count_2011

# Function to get total registered users by day
def total_registered_df(day_df):
    reg_df = day_df.groupby(by="dteday").agg({"registered": "sum"})
    reg_df = reg_df.reset_index()
    reg_df.rename(columns={"registered": "register_sum"}, inplace=True)
    return reg_df

# Function to get total orders by hour
def total_order_by_hour(hour_df):
    total_order_items_df = hour_df.groupby("hr").count_cr.sum().sort_values(ascending=False).reset_index()
    return total_order_items_df

# Function to get weather situation data
def weather_situation(day_df):
    weather_df = day_df.groupby(by="weather_situation").agg({"count_cr": "sum"})
    return weather_df

# Function to create monthly rent data
def create_monthly_rent_df(df):
    monthly_rent_df = df.groupby(by='month').agg({'count_cr': 'sum'})
    ordered_months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    monthly_rent_df = monthly_rent_df.reindex(ordered_months, fill_value=0)
    return monthly_rent_df

# Function to create working day rent data
def create_workingday_rent_df(df):
    workingday_rent_df = df.groupby(by='workingday').agg({'count_cr': 'sum'}).reset_index()
    return workingday_rent_df

# Function to get total casual users by day
def total_casual_df(day_df):
    cas_df = day_df.groupby(by="dteday").agg({"casual": ["sum"]})
    cas_df = cas_df.reset_index()
    cas_df.rename(columns={"casual": "casual_sum"}, inplace=True)
    return cas_df

# Function to get season data
def macem_season(day_df):
    season_df = day_df.groupby(by="season").count_cr.sum().reset_index()
    return season_df

# Load data
days_df = pd.read_csv("dashboard/day_fix.csv")
hours_df = pd.read_csv("dashboard/hour_fix.csv")

datetime_columns = ["dteday"]
days_df.sort_values(by="dteday", inplace=True)
days_df.reset_index(inplace=True)

hours_df.sort_values(by="dteday", inplace=True)
hours_df.reset_index(inplace=True)

for column in datetime_columns:
    days_df[column] = pd.to_datetime(days_df[column])
    hours_df[column] = pd.to_datetime(hours_df[column])

min_date_days = days_df["dteday"].min()
max_date_days = days_df["dteday"].max()

min_date_hour = hours_df["dteday"].min()
max_date_hour = hours_df["dteday"].max()

with st.sidebar:
    st.image("https://thumbs.dreamstime.com/b/bike-sharing-system-icons-mobile-application-vector-closeup-set-signs-flat-illustration-136558853.jpg?w=768")
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        min_value=min_date_days,
        max_value=max_date_days,
        value=[min_date_days, max_date_days]
    )

main_df_days = days_df[(days_df["dteday"] >= str(start_date)) & (days_df["dteday"] <= str(end_date))]
main_df_hour = hours_df[(hours_df["dteday"] >= str(start_date)) & (hours_df["dteday"] <= str(end_date))]

hour_count_df = get_total_count_by_hour_df(main_df_hour)
weather_df = weather_situation(main_df_days)
day_df_count_2011 = count_by_day_df(main_df_days)
reg_df = total_registered_df(main_df_days)
cas_df = total_casual_df(main_df_days)
monthly_rent_df = create_monthly_rent_df(main_df_days)
workingday_rent_df = create_workingday_rent_df(main_df_days)
total_order_hour_df = total_order_by_hour(main_df_hour)
season_df = macem_season(main_df_hour)

st.header('Bike Sharing :sparkles:')

st.subheader('Daily Sharing')
col1, col2, col3 = st.columns(3)

with col1:
    total_orders = day_df_count_2011.count_cr.sum()
    st.metric("Total Sharing Bike", value=total_orders)

with col2:
    total_sum = reg_df.register_sum.sum()
    st.metric("Total Registered", value=total_sum)

with col3:
    total_sum = cas_df.casual_sum.sum()
    st.metric("Total Casual", value=total_sum)

# Plot for the hours with the most and least bike rentals
st.subheader("pada jam berapa yang paling banyak dan paling sedikit disewa?")
fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(35, 15))

sns.barplot(
    x="hr", 
    y="count_cr", 
    data=total_order_hour_df.head(5), 
    palette=["#D3D3D3", "#D3D3D3", "#90CAF9", "#D3D3D3", "#D3D3D3"], 
    ax=ax[0]
)
ax[0].set_ylabel(None)
ax[0].set_xlabel("Hours (PM)", fontsize=30)
ax[0].set_title("Jam dengan banyak penyewa sepeda", loc="center", fontsize=30, pad=20)
ax[0].tick_params(axis='y', labelsize=35)
ax[0].tick_params(axis='x', labelsize=30)

sns.barplot(
    x="hr", 
    y="count_cr", 
    data=total_order_hour_df.sort_values(by="hr", ascending=True).head(5), 
    palette=["#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#90CAF9"], 
    ax=ax[1]
)
ax[1].set_ylabel(None)
ax[1].set_xlabel("Hours (AM)", fontsize=30)
ax[1].set_title("Jam dengan sedikit penyewa sepeda", loc="center", fontsize=30, pad=20)
ax[1].invert_xaxis()
ax[1].yaxis.set_label_position("right")
ax[1].yaxis.tick_right()
ax[1].tick_params(axis='y', labelsize=35)
ax[1].tick_params(axis='x', labelsize=30)

st.pyplot(fig)

# Plot for the impact of weather on bike rentals
st.subheader("Pengaruh Cuaca terhadap Jumlah Penyewa Sepeda")

fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    x=weather_df.index, 
    y=weather_df['count_cr'], 
    palette=["#90CAF9", "#D3D3D3", "#D3D3D3"],
    ax=ax
)
for index, row in enumerate(weather_df['count_cr']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.set_xlabel(None)
ax.set_ylabel(None)
ax.tick_params(axis='x', labelsize=20)
ax.tick_params(axis='y', labelsize=15)
st.pyplot(fig)

# Plot for monthly bike rentals
st.subheader('Monthly Rentals')
fig, ax = plt.subplots(figsize=(24, 8))
ax.plot(
    monthly_rent_df.index,
    monthly_rent_df['count_cr'],
    marker='o', 
    linewidth=2,
    color='tab:blue'
)

for index, row in enumerate(monthly_rent_df['count_cr']):
    ax.text(index, row + 1, str(row), ha='center', va='bottom', fontsize=12)

ax.tick_params(axis='x', labelsize=25, rotation=45)
ax.tick_params(axis='y', labelsize=20)
st.pyplot(fig)

# Plot for bike rentals by working day
st.subheader('Rentals by Working Day')
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(
    x=workingday_rent_df['workingday'],
    y=workingday_rent_df['count_cr'],
    palette=["#90CAF9", "#D3D3D3"],
    ax=ax
)
for index, row in workingday_rent_df.iterrows():
    ax.text(index, row['count_cr'] + 1, str(row['count_cr']), ha='center', va='bottom', fontsize=12)

ax.set_xlabel('Working Day', fontsize=15)
ax.set_ylabel('Count', fontsize=15)
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12)
st.pyplot(fig)

# Plot for bike rentals by season
st.subheader("musim apa yang paling banyak disewa?")

colors = ["#D3D3D3", "#D3D3D3", "#D3D3D3", "#90CAF9"]
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    y="count_cr", 
    x="season",
    data=season_df.sort_values(by="season", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("Grafik Antar Musim", loc="center", fontsize=50)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=35)
ax.tick_params(axis='y', labelsize=30)
st.pyplot(fig)

# Pie chart for comparison of registered and casual users
st.subheader("Perbandingan Customer yang Registered dengan casual")

labels = 'casual', 'registered'
sizes = [18.8, 81.2]
explode = (0, 0.1)

fig1, ax1 = plt.subplots()
ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%', colors=["#D3D3D3", "#90CAF9"], shadow=True, startangle=90)
ax1.axis('equal')

st.pyplot(fig1)
