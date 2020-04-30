from plotly.offline import plot
from plotly.subplots import make_subplots
from django.shortcuts import render

import numpy as np
import pandas as pd
import plotly
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio
pio.templates.default = "plotly_dark"

data = pd.read_csv("train.csv", parse_dates=['Date'])
cleaned_data = pd.read_csv(
    "covid_19_clean_complete.csv", parse_dates=['Date'])
cases = ['Confirmed', 'Deaths', 'Recovered', 'Active']
cleaned_data['Active'] = cleaned_data['Confirmed'] - \
    cleaned_data['Deaths'] - cleaned_data['Recovered']
cleaned_data['Country/Region'] = cleaned_data['Country/Region'].replace(
    'Mainland China', 'China')
cleaned_data[['Province/State']
             ] = cleaned_data[['Province/State']].fillna('')
cleaned_data[cases] = cleaned_data[cases].fillna(0)
cleaned_data.rename(columns={'Date': 'date'}, inplace=True)
data = cleaned_data
formated_gdf = data.groupby(
    ['date', 'Country/Region'])['Confirmed', 'Deaths'].max()
formated_gdf = formated_gdf.reset_index()
formated_gdf['date'] = pd.to_datetime(formated_gdf['date'])
formated_gdf['date'] = formated_gdf['date'].dt.strftime('%m/%d/%Y')
formated_gdf['size'] = formated_gdf['Confirmed'].pow(0.3)

fig1 = px.scatter_geo(formated_gdf, locations="Country/Region", locationmode='country names',
                      color="Confirmed", size='size', hover_name="Country/Region",
                      range_color=[0, 1500],
                      projection="natural earth", animation_frame="date",
                      title='COVID-19: Spread Over Time', color_continuous_scale="portland")
plot_div1 = plot(fig1, output_type='div', include_plotlyjs=False, show_link=False,
                 link_text="", image_width=500, config={"displaylogo": False})
fig2 = px.scatter_geo(formated_gdf, locations="Country/Region", locationmode='country names',
                      color="Deaths", size='size', hover_name="Country/Region",
                      range_color=[0, 100],
                      projection="natural earth", animation_frame="date",
                      title='COVID-19: Deaths Over Time', color_continuous_scale="peach")
plot_div2 = plot(fig2, output_type='div', include_plotlyjs=False, show_link=False,
                 link_text="", image_width=500, config={"displaylogo": False})

data['Province/State'] = data['Province/State'].fillna('')
temp = data[[col for col in data.columns if col != 'Province/State']]

latest = temp[temp['date'] == max(temp['date'])].reset_index()
latest_grouped = latest.groupby(
    'Country/Region')['Confirmed', 'Deaths'].sum().reset_index()
fig3 = px.bar(latest_grouped.sort_values('Confirmed', ascending=False)[:30][::-1],
              x='Confirmed', y='Country/Region',
              title='Confirmed Cases Worldwide', text='Confirmed', height=1000, orientation='h')
plot_div3 = plot(fig3, output_type='div', include_plotlyjs=False, show_link=False,
                 link_text="", image_width=500, config={"displaylogo": False})


def index(request):
    global plot_div1, plot_div2
    return render(request, "index.html", context={'plot_div1': plot_div1, 'plot_div2': plot_div2, 'plot_div3': plot_div3})


def about(request):
    return render(request, "abhi.html")


data['Province/State'] = data['Province/State'].fillna('')
temp = data[[col for col in data.columns if col != 'Province/State']]

latest = temp[temp['date'] == max(temp['date'])].reset_index()
latest_grouped = latest.groupby(
    'Country/Region')['Confirmed', 'Deaths'].sum().reset_index()
fig3 = px.bar(latest_grouped.sort_values('Confirmed', ascending=False)[:30][::-1],
              x='Confirmed', y='Country/Region',
              title='Confirmed Cases Worldwide', text='Confirmed', height=1000, orientation='h')
