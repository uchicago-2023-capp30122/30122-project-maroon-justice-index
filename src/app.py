# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import geopandas as gpd
import numpy as np

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# ----------------------- data and maps here -----------------------------------

# --------- census tract pp index map ----------------

census_tracts_df = gpd.read_file("boundaries_census_tracts_2010.geojson")
df = pd.read_json("index_draft_disposable_income_sex_age.json")

# figure
fig1 = px.choropleth_mapbox(df, 
                           geojson = census_tracts_df, 
                           locations = "tract",
                           color="pp_index",
                           color_continuous_scale="amp",
                           range_color=(0, 20.7),
                           featureidkey="properties.tractce10",
                           mapbox_style="carto-positron",
                           opacity=0.5,
                           hover_name="NAME",
                           center={"lat": 41.8781, "lon": -87.6298},
                           zoom=9)
fig1.update_geos(fitbounds="locations",visible=False)
fig1.update_layout(title_text='Period Poverty Index by Census Tract', title_x=0.5,
    margin={"r":0,"t":40,"l":0,"b":0},
    legend=dict(
        yanchor="bottom",
            y=0.99,
            xanchor="left",
            x=0.01
            ))

# ---------------- community centers map --------------------

df2 = pd.read_csv("geocoded_community_centers_chicago.csv")
geometry = gpd.points_from_xy(df2['lon'], df2['lat'])
gdf = gpd.GeoDataFrame(df2, geometry=geometry)

fig2 = px.scatter_mapbox(gdf, 
                        lat=gdf.geometry.y, 
                        lon=gdf.geometry.x, 
                        zoom=10,
                        hover_name="Name",
                        color="Type",
                        mapbox_style="carto-positron",
                        opacity=0.5)
fig2.update_layout(title_text='Women and Girls Community Centers in Chicago', title_x=0.5,
    margin={"r":0,"t":40,"l":0,"b":0})

# neighborhoods = "https://raw.githubusercontent.com/blackmad/neighborhoods/master/chicago.geojson"

# --------------------------- html page layout here ----------------------------

app.layout = dbc.Container([

    # header
    dbc.Row([
        dbc.Col([
            html.Br(), # add space above header
            html.H1('Mapping Period Poverty in Chicago', style={'text-align':'center'}),
            html.P('Betty Fang, Diamon Dunlap, Ivanna Rodríguez, Jimena Salinas', 
            style={'text-align':'center', 'font-style':'italic'}),
        ], width=12) # align supposed to add padding but not working
    ], align='end'),

    # intro
    dbc.Row([
        dbc.Col([
            html.Br(),
            html.P(['Lorem ipsum dolor sit amet, consectetur adipiscing elit, \
            sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. \
            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris \
            nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in \
            reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla\
            pariatur. Excepteur sint occaecat cupidatat non proident, sunt in\
             culpa qui officia deserunt mollit anim id est laborum.',
            html.Br(), 'now I am adding a new line break but does this text appear??']),
        ], width=12) # 12 is maximum you can take
    ], align='end'),

    # index methodology (?)

    # index map
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='graph',
                figure = fig1)
        ], width=12)
    ], align='center'),

    # community centers text
    dbc.Row([
        dbc.Col([
            html.Br(), # add space above header
            html.P(['Lorem ipsum dolor sit amet, consectetur adipiscing elit, \
            sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. \
            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris \
            nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in \
            reprehenderit in voluptate velit esse cillum dolore eu fugiat \
            nulla pariatur. Excepteur sint occaecat cupidatat non proident, \
            sunt in culpa qui officia deserunt mollit anim id est laborum.\
            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris \
            nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in \
            reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla\
            pariatur. Excepteur sint occaecat cupidatat non proident, sunt in\
            culpa qui officia deserunt mollit anim id est laborum. \
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, \
            sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. \
            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris \
            nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in \
            reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla\
            pariatur. Excepteur sint occaecat cupidatat non proident, sunt in'])
        ], width = 12, align='end') # how do u add padding...?
    ], align='end'),

    # community centers map
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='graph1',
                figure = fig2)
        ], width=12)
    ], align='center'),

    # community centers text
    dbc.Row([
        dbc.Col([
            html.Br(), # add space above header
            html.P(['Lorem ipsum dolor sit amet, consectetur adipiscing elit, \
            sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. \
            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris \
            nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in \
            reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla\
            pariatur. Excepteur sint occaecat cupidatat non proident, sunt in\
            culpa qui officia deserunt mollit anim id est laborum. \
            Lorem ipsum dolor sit amet, consectetur adipiscing elit, \
            sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. \
            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris \
            nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in \
            reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla\
            pariatur. Excepteur sint occaecat cupidatat non proident, sunt in\
             culpa qui officia deserunt mollit anim id est laborum.',
            html.Br(), 'now I am adding a new line break but does this text appear??']),
        ], width=12) # 12 is maximum you can take
    ], align='end')
])

if __name__ == '__main__':
    app.run_server(debug=True)
