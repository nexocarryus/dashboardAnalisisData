import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import streamlit as st


# Helper function yang dibutuhkan untuk menyiapkan berbagai dataframe
def create_bySeason_df(df):

    season_names = {
        1: 'Springer', 
        2: 'Summer', 
        3: 'Fall', 
        4: 'Winter'
    }


    seasonal_trends = df.groupby('season')[['cnt']].sum().reset_index()
    seasonal_trends['season'] = seasonal_trends['season'].map(season_names)
    seasonal_trends = seasonal_trends.sort_values(by='cnt')

    return seasonal_trends

def create_byWeather(df):
    weather_names = {
    1: 'Clear', 
    2: 'Mist', 
    3: 'Light snow', 
    4: 'Heavy Rain'
    }

    weather_trends = df.groupby('weathersit')[['cnt']].sum().reset_index()
    weather_trends['weathersit'] = weather_trends['weathersit'].map(weather_names)
    weather_trends = weather_trends.sort_values(by='cnt')
    return weather_trends

def create_byDay(df):
    
    weekday_names = {
        0: "Sunday",
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday"
    }


    day_trends = df.groupby('weekday')[['cnt']].sum().reset_index()
    day_trends['weekday'] = day_trends['weekday'].map(weekday_names)  
    day_trends = day_trends.sort_values(by='cnt')

    return day_trends

def createUserPattern_byHour(df):
    hourly_rentals = df.groupby('hr')[['casual', 'registered']].mean().reset_index()
    return hourly_rentals

def createTrend_byMonth(df):
    df['month'] = df['dteday'].dt.month
    monthly_trends = df.groupby('month')[['casual', 'registered', 'cnt']].sum().reset_index()
    return monthly_trends

def createPattern_byHourandDay(df):

    
    weekday_names = {
        0: "Sunday",
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday"
    }
    
    hourly_weekday_rentals = df.groupby(['hr', 'weekday'])['cnt'].sum().reset_index()
    pivot_table = hourly_weekday_rentals.pivot(index='hr', columns='weekday', values='cnt')
    pivot_table.columns = pivot_table.columns.map(weekday_names)
    return pivot_table

def create_byHourandWeek(df):
    hourly_weekday_rentals = df.groupby(['hr', 'weekday'])['cnt'].sum().reset_index()
    pivot_table = hourly_weekday_rentals.pivot(index='hr', columns='weekday', values='cnt')

    weekday_names = {
        0: "Sunday",
        1: "Monday",
        2: "Tuesday",
        3: "Wednesday",
        4: "Thursday",
        5: "Friday",
        6: "Saturday"
    }
    pivot_table.columns = pivot_table.columns.map(weekday_names)
    return pivot_table

with st.sidebar:
    #menambahkan logo perusahaan
    st.image("RentBikeLogo.png")

# Load cleaned data
df_day = pd.read_csv("df_dayClean.csv")
df_day['dteday'] = pd.to_datetime(df_day['dteday'])
df_hour = pd.read_csv("df_hourClean.csv")

# # Menyiapkan berbagai dataframe
bySeason_df = create_bySeason_df(df_day)
byWeather_df = create_byWeather(df_day)
byDay_df = create_byDay(df_day)
userbyHour = createUserPattern_byHour(df_hour)
byHourandWeek_df = create_byHourandWeek(df_hour)


#menampilkan header dashboard
st.header('Welcome to Rental Bike dashboard :sparkles:')
st.subheader('Bike Rental Peak')

#puncak sewa sepeda berdasarkan season, cuaca, dan hari
colPeakSeason, colPeakWeather, colPeakDay = st.columns(3)


with colPeakSeason:

    colors = ['lightgrey' if cnt != bySeason_df['cnt'].max() else 'lightgreen' for cnt in bySeason_df['cnt']]
    plt.figure(figsize=(34, 30))
    sns.barplot(x='season', y='cnt', data=bySeason_df, palette=colors)
    plt.xlabel('Musim')
    plt.ylabel('Total penyewa sepeda')
    plt.title('berdasarkan musim')
    st.pyplot(plt)

with colPeakWeather:
    
    colors = ['lightgrey' if cnt != byWeather_df['cnt'].max() else 'lightgreen' for cnt in byWeather_df['cnt']]
    plt.figure(figsize=(34, 30))
    sns.barplot(x='weathersit', y='cnt', data=byWeather_df, palette=colors)
    plt.xlabel('Cuaca')
    plt.ylabel('Total penyewa sepeda')
    plt.title('berdasarkan cuaca')
    st.pyplot(plt)

with colPeakDay:
    
    colors = ['lightgrey' if cnt != byDay_df['cnt'].max() else 'lightgreen' for cnt in byDay_df['cnt']]
    plt.figure(figsize=(34, 30))
    sns.barplot(x='weekday', y='cnt', data=byDay_df, palette=colors)  
    plt.xlabel('')
    plt.ylabel('')
    plt.title('berdasarkan hari')
    plt.xticks(rotation=20, ha='right')
    st.pyplot(plt)

#pola penyewaan sepeda registered user vs casual user
st.subheader('Pattern of user')

plt.figure(figsize=(50, 20))
plt.plot(userbyHour['hr'], userbyHour['casual'], label='Casual', color='blue', linewidth=2.5)
plt.plot(userbyHour['hr'], userbyHour['registered'], label='Registered', color = 'green', linewidth=2.5)
plt.xlabel('Jam dalam sehari', size = 50)
plt.ylabel('Rata rata penyewaan sepeda', size = 50)
plt.title('Registered user vs casual user berdasarkan jam', size = 60)
plt.legend()
plt.grid(True)
st.pyplot(plt)

plt.figure(figsize=(50, 40))
sns.scatterplot(x='temp', y='casual', data=df_day, color='blue', label='Casual', alpha=0.7, s=200)
sns.scatterplot(x='temp', y='registered', data=df_day, color='green', label='Registered', alpha=0.7, s=200)
plt.xlabel('Temperatur (celcius)')
plt.ylabel('Penyewaan sepeda')
plt.title('Registered user vs casual user berdasarkan temperatur')
plt.legend()
plt.grid(True)
st.pyplot(plt)

weather_names = {
    1: 'Clear', 
    2: 'Mist', 
    3: 'Light snow', 
    4: 'Heavy Rain'
}

plt.figure(figsize=(50, 20))
sns.boxplot(x='weathersit', y='casual', data=df_day, color='blue', label='Casual')
sns.boxplot(x='weathersit', y='registered', data=df_day, color='lightgreen', label='Registered')

xticklabels = plt.gca().get_xticklabels()

for label in xticklabels:
    label.set_text(weather_names.get(int(label.get_text()), label.get_text()))

plt.gca().set_xticklabels(xticklabels)
plt.xlabel('')
plt.ylabel('')
plt.title('Penyewaan sepeda registered user vs casual user berdasarkan cuaca')
plt.legend()
st.pyplot(plt)

#trend penyewaan sepeda dari tahun 2011 sampai tahun 2012
st.subheader('Bike rental trend from 2011-2012')
plt.figure(figsize=(40, 20))
plt.plot(df_day['dteday'], df_day['cnt'], color='green')
plt.xlabel('Date', size=15)
plt.ylabel('Count', size=15)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m')) 
plt.gca().xaxis.set_major_locator(mdates.MonthLocator(interval=1))  
plt.xticks(rotation=45, ha='right')
plt.tight_layout() 
st.pyplot(plt)

df_day['month'] = df_day['dteday'].dt.month
monthly_trends = df_day.groupby('month')[['casual', 'registered', 'cnt']].sum().reset_index()

plt.figure(figsize=(50, 20))
plt.plot(monthly_trends['month'], monthly_trends['casual'], label='Casual', marker='o', color='blue',  linewidth=2.5)
plt.plot(monthly_trends['month'], monthly_trends['registered'], label='Registered', marker='o', color = 'green',  linewidth=2.5)
plt.plot(monthly_trends['month'], monthly_trends['cnt'], label='Total', marker='o', color='orange',  linewidth=2.5)
plt.xlabel('bulan')
plt.ylabel('')
plt.title('tren penyewaan sepeda berdasarkan bulan')
plt.xticks(monthly_trends['month'])
plt.legend()
plt.grid(True)
st.pyplot(plt)

#pola volume penyewaan sepeda berdasarkan jam dan hari
st.subheader('Bike rental volume pattern')
plt.figure(figsize=(50, 40))
sns.heatmap(byHourandWeek_df, annot=True, fmt="d", cmap="YlGnBu")
plt.title('Volume rental sepeda berdasarkan jam dan hari')
plt.ylabel('Jam')
plt.xlabel('')
st.pyplot(plt)





