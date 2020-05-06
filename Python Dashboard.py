
# coding: utf-8

# In[1]:

import dash, dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from sorted_months_weekdays import *
from sort_dataframeby_monthorweek import *

# In[2]:

df_shoot = pd.read_csv(r'https://github.com/munjasolanke/Dashboard-data-for-DV/massshoot_data.csv')
df_shoot['Incident Date'] = pd.to_datetime(df_shoot['Incident Date'])
external_stylesheets = ['https://github.com/munjasolanke/Dashboard.github.io/learn.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


# In[4]:


df_19 = df_shoot[df_shoot['Year']==2019]
df19=df_19.groupby('Month')[['Killed']].sum().reset_index()

df19=Sort_Dataframeby_MonthandNumeric_cols(df = df19, monthcolumn='Month',numericcolumn='Killed')

df191=df_19.groupby('Month')[['Injured']].sum().reset_index()

df191=Sort_Dataframeby_MonthandNumeric_cols(df = df191, monthcolumn='Month',numericcolumn='Injured')

df_2020 = df_shoot[df_shoot['Year']==2020]
df20=df_2020.groupby('Month')[['Killed']].sum().reset_index()

df20=Sort_Dataframeby_MonthandNumeric_cols(df = df20, monthcolumn='Month',numericcolumn='Killed')

df201=df_2020.groupby('Month')[['Injured']].sum().reset_index()

df201=Sort_Dataframeby_MonthandNumeric_cols(df = df201, monthcolumn='Month',numericcolumn='Injured')


# In[7]:


import folium
map_usa = folium.Map(location=[37.0902, -95.7129],zoom_start=4)
for lat, lng, city, state, killed, injured, month in zip(df_19['Latitude'], df_19['Longitude'], df_19['City Or County'],df_19['State'], df_19['Killed'], df_19['Injured'], df_19['Month']):
    label = 'City: {}, State:{}, Killed: {}, Injured: {}, Month:{}'.format(city,state,killed,injured, month)
    folium.CircleMarker(
        [lat, lng],
        radius=injured,
        popup=label,
        color='red',
        fill=True,
        fill_color='red',
        fill_opacity=0.1,
        parse_html=False).add_to(map_usa)


# In[10]:


app.layout = html.Div(children=[html.H1(children='Python Dash',style={'textAlign':'center'}),
                                html.H1(children='Gun Violence cases in USA',style={'textAlign':'center'}),
                                dash_table.DataTable(columns=[{'name':i,'id':i} for i in df_shoot.columns], data=df_shoot.head().to_dict('records'),),
                               dcc.Graph(figure={'data':[
                                   {'x':df191.Month,'y':df191.Injured, 'type':'bar','name':'Injured'},
                                   {'x':df19.Month,'y':df19.Killed, 'type':'bar','name':'Killed'},],
                                                'layout': {'title': '2019 Violence'}}),
                               dcc.Graph(figure={'data':[
                                   {'x':df201.Month,'y':df201.Injured, 'type':'bar','name':'Injured'},
                                   {'x':df20.Month,'y':df20.Killed, 'type':'bar','name':'Killed'},],
                                                'layout': {'title': '2020 Violence'}}),
                               html.Div([html.H3(children='2019 Gun Violence',style={'textAlign':'center'}),html.Iframe(srcDoc=open('t.html','r').read(),width='100%',height='600')]),
                               html.Div([html.H3(children='2020 Gun Violence',style={'textAlign':'center'}), html.Iframe(srcDoc=open('t2.html','r').read(),width='100%',height='600')])])
                               
                                 


# In[13]:


if __name__ == '__main__':
    app.run_server(debug=False)

