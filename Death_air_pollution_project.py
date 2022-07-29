import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import requests
import streamlit as st
from streamlit_lottie import st_lottie

st.set_page_config(
    page_title="Deaths due to Air Pollution",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.header('Deaths due to Air Pollution')

csv = r'C:\Users\asus\Desktop\death-rates-from-air-pollution.csv'
air_poll_df = pd.read_csv(csv, sep=',')
st.download_button(
     label="Download data as CSV",
     data=csv,
     file_name='Deaths_air_pollution.csv',
     mime='text/csv',
 )

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
col_1, col_2 = st.columns([3, 1])
with col_1:
    st.write("""

INTRODUCTION

Air Pollution has always been at the center of many debates and issues during 
the years as it continues to be the reason for the killing of innocent lives in the
world. What would be really interesting to analyse trough data and statistics,
is how air pollution has change over the last decades by analyzing deaths per
100k (caused by pollution). 

Moreover let's see the countries that suffered
from it the most and the differences in how outdoor, indoor and ozone
pollution is affecting the population.

""")
with col_2:
    lottie_pollution = load_lottieurl("https://assets3.lottiefiles.com/packages/lf20_iwWWLK.json")
    st_lottie(lottie_pollution)

st.sidebar.subheader('Controls')
st.sidebar.download_button('Download data as CSV', csv, file_name='Deaths_air_pollution.csv')

show_raw_data = st.sidebar.checkbox('Show raw data')
if show_raw_data:
    st.subheader('Raw data')
    st.write(air_poll_df)

data_dictionary = st.sidebar.checkbox('Data dictionary')
if data_dictionary:
    st.subheader('Data dictionary')
    st.markdown(
        """
        * **Entity**: It contains the name of the country or the region.
        * **Code**: It contain Code of the country.
        * **Year**: Years range from 1990 to 2017
        * **Air pollution (total) (deaths per 100,000)** : Contains total deaths.
        * **Indoor air pollution (deaths per 100,000)** : Contains deaths due to indoor air pollution.
        * **Outdoor particulate matter (deaths per 100,000)** : Contains deaths due to outdoor pollution.
        * **Outdoor ozone pollution (deaths per 100,000)** : Deaths due to ozone pollution
        """)

air_poll_df[air_poll_df.Code.isna()]['Entity'].unique()
world_region_df = air_poll_df[air_poll_df.Code.isna()]
world_region_df.head()
world_region_df_index = world_region_df.set_index('Entity')

#dataframe containing rows only for world regions
world_region_df_index.drop(['Caribbean', 'Central Europe, Eastern Europe, and Central Asia', 'England',
       'High SDI', 'High-income', 'High-income Asia Pacific',
       'High-middle SDI', 'Latin America and Caribbean', 'Low SDI',
       'Low-middle SDI', 'Middle SDI','Scotland', 'Wales'], inplace=True)
world_region_df = world_region_df_index.reset_index()
world_region_df.drop(columns='Code', inplace=True)

#dataframe containing rows only for individual countries
air_poll_df.set_index('Entity', inplace=True)
air_poll_df.drop(['Andean Latin America', 'Australasia','Caribbean', 'Central Asia',
       'Central Europe',
       'Central Europe, Eastern Europe, and Central Asia',
       'Central Latin America', 'Central Sub-Saharan Africa', 'East Asia',
       'Eastern Europe', 'Eastern Sub-Saharan Africa','England',
       'High SDI', 'High-income', 'High-income Asia Pacific',
       'High-middle SDI', 'Latin America and Caribbean', 'Low SDI',
       'Low-middle SDI', 'Middle SDI', 'North Africa and Middle East',
       'North America', 'Northern Ireland', 'Oceania', 'Scotland',
       'South Asia', 'Southeast Asia',
       'Southeast Asia, East Asia, and Oceania', 'Southern Latin America',
       'Southern Sub-Saharan Africa', 'Sub-Saharan Africa',
       'Tropical Latin America', 'Wales', 'Western Europe',
       'Western Sub-Saharan Africa', 'World'], inplace=True)
air_poll_df.reset_index(inplace=True)
air_poll_df.info()

#show data manipulated datasets
manipulated_data = st.sidebar.checkbox('Show manipulated data')
if manipulated_data:
    st.subheader('Manipulated data')
    st.write('Before proceeding further with the visualization, I cleaned the dataset from Null values when necessary '
             'and filtered it by creating two new sub-datasets that will be useful in our analysis. ')
    st.write('Dataset containing rows only for individual countries:')
    st.write(air_poll_df)
    st.write('Dataset containing rows only for world regions:')
    st.write(world_region_df)

#Visualization idioms
plt.figure(figsize=(15,6))
st.subheader("Air Pollution (Deaths per 100k) tot and by type")
col_1, col_2 = st.columns(2)
with col_1:
    fig, ax = plt.subplots(figsize=(10, 6))
    st.caption('**Air Pollution tot (deaths per 100k)**')
    tot_poll_df = air_poll_df.groupby('Year').mean().iloc[:, 0]
    tot_poll_df.plot()
    ax.set_xlabel('Year')
    ax.set_ylabel('Air Pollution (deaths per 100k)')
    st.pyplot(fig)

with col_2:
    fig, ax = plt.subplots(figsize=(10, 6))
    st.caption('**Air pollution by type**')
    plt.plot(air_poll_df.groupby('Year').mean().iloc[:, 1], label='indoor')
    plt.plot(air_poll_df.groupby('Year').mean().iloc[:, 2], label='outdoor')
    plt.plot(air_poll_df.groupby('Year').mean().iloc[:, 3], label='ozone')
    plt.legend()
    ax.set_xlabel('Year')
    ax.set_ylabel('Air Pollution (deaths per 100k)')
    st.pyplot(fig)
st.write('In all cases, we see a clear reduction in worldwide deaths due to air pollution.')
st.write("Let's see if this holds true for the same plot by region.")


fig = plt.subplots(figsize=(10, 6))
fig = px.line(world_region_df, x="Year", y="Air pollution (total) (deaths per 100,000)", color='Entity',hover_data={'Year':False}, width=950, height=500)
st.write(fig)
st.write('Even though it is quite messy, there is in almost every case a downward trend.')

air_poll_df['Year'].unique()
poll_df = air_poll_df.query('Year == 2017')

fig= plt.subplots(figsize=(10, 6))
st.subheader('Air pollution tot - top 10 countries with values higher than 100,000 - Year 2017')
top_10 = poll_df[poll_df['Air pollution (total) (deaths per 100,000)'] > 100.000].sort_values(by='Air pollution (total) (deaths per 100,000)', ascending=False)[0:10]
fig = px.bar(top_10, y='Air pollution (total) (deaths per 100,000)', x='Entity', text='Air pollution (total) (deaths per 100,000)', color='Entity', width=800, height=520)
fig.update_traces(texttemplate='%{text:.4s}', textposition='outside')
fig.update_layout(xaxis_tickangle=-45)
st.write(fig)

st.subheader('Air pollution (total) (deaths per 100,000)')
select_year = st.selectbox('Select Year:', air_poll_df['Year'].unique())
poll_df = air_poll_df[air_poll_df['Year'] == select_year]



fig, ax = plt.subplots(figsize=(10, 6))
fig = px.choropleth(poll_df, locations="Code",
                    hover_name="Entity",
                    color="Air pollution (total) (deaths per 100,000)",
                    title = "Air pollution",  color_continuous_scale=px.colors.sequential.PuRd)
fig.update_layout(width=1000, height=600, margin=dict(l=0, r=0, t=0, b=0))
st.write(fig)

with st.expander('Show Animated Choropleth'):
    st.subheader('Animated Choropleth')
    fig, ax = plt.subplots(figsize=(25, 10))
    fig = px.choropleth(air_poll_df, locations="Code",
                    hover_name="Entity",
                    color="Air pollution (total) (deaths per 100,000)",
                    animation_frame="Year",
                    title = "Air pollution",  color_continuous_scale=px.colors.sequential.PuRd)
    fig.update_layout(width=850, height=450, margin={"r":0,"t":0,"l":0,"b":0})
    st.write(fig)