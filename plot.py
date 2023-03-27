#import streamlit as st
#import streamlit.components.v1 as stc

import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import math

# Load data, define hover text and bubble size
df = pd.read_excel("gactbook.xlsx")

hover_text = []
bubble_size = []

for index, row in df.iterrows():
    hover_text.append(('Country : {country}<br>'+
                      'Continent : {continent}<br>'+
                      'Life Expectancy : {lifeExp}<br>'+
                      'GDP per capita : {gdp}<br>'+
                      'Population : {pop}').format(country=row['Country'],
                                            continent=row['Continent'],
                                            lifeExp=row['Life expectancy at birth'],
                                            gdp=row['GDP per capita '],
                                            pop=row['Population ']))
    bubble_size.append(math.sqrt(row['Population ']))

df['text'] = hover_text
df['size'] = bubble_size
sizeref = 2.*max(df['size'])/(5000)

# Dictionary with dataframes for each continent
continent_names = ['Asia', 'Europe', 'North America', 'South America', 'Africa', 'Oceania']
continent_data = {continent:df.query("Continent == '%s'" %continent)
                              for continent in continent_names}

# Define color scale for each continent
color_map = {"Asia": '#003f5c',"Europe" : '#58508d', "North America" : '#bc5090',
             "South America" : '#ff6361', "Africa" : '#ffa600', "Oceania" : '#8f8160'}

# Create figure
fig = go.Figure()

for continent_name, continent in continent_data.items():
    fig.add_trace(go.Scatter(
        x=continent['GDP per capita '], y=continent['Life expectancy at birth'],
        name=continent_name, text=continent['text'],
        marker_size=continent['size'], marker_color=color_map[continent_name]))

# Tune marker appearance and layout
fig.update_traces(mode='markers', marker=dict(sizemode='area',
                                              sizeref=sizeref, line_width=2))

fig.update_layout(
    title='Life Expectancy vs GDP per Capita',
    xaxis=dict(
        title='GDP per capita',
        gridcolor='white',
        type='log',
        gridwidth=2,
    ),
    yaxis=dict(
        title='Life Expectancy',
        gridcolor='white',
        gridwidth=2,
    ),
    #plot_bgcolor='rgb(243, 243, 243)',
)
fig.show()