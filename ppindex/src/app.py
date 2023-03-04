'''
This app renders the Dash application for our project

Run this app with `python3 src/app.py` and visit
http://127.0.0.1:8050/ in your web browser.

Author: Ivanna
Date: 3/3/2023
'''

from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import geopandas as gpd
import numpy as np

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# ----------------------- data and maps here -----------------------------------
L_FONT = "Work Sans, sans-serif"
LT_SIZE = 16
L_SIZE = 12

# --------- census tract pp index map ----------------

census_tracts = gpd.read_file("ppindex/src/boundaries_census_tracts_2010.geojson")
df = pd.read_json("ppindex/src/index_w_neigh_names.json")
df = df.rename(columns={'tract':'Census Tract', 'pp_index':'Period Poverty Index'})

def create_idx_maps(df, gdf, zoom, lat, lon):
    '''
    this function creates the period poverty index choropleth

    inputs: df (pandas dataframe)
            gdf (geopandas dataframe)
            zoom (int) zoom level for displaying map
            lat (int) latitute for displaying map 
            lon (lon) longitude for displaying map
    output: choropleth map (plotly express class)
    '''

    fig = px.choropleth_mapbox(
        df, 
        geojson = census_tracts, 
        locations = "Census Tract", 
        featureidkey="properties.tractce10",
        color="Period Poverty Index", color_continuous_scale="amp", 
               range_color=(0, 20.7), 
        mapbox_style="carto-positron", opacity=0.5,
        hover_name="neighborhood_name",
        center={"lat": lat, "lon": lon}, zoom=zoom)

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        title_x=0.5,
        font=dict(family=L_FONT), 
        margin={"r":0,"t":0,"l":0,"b":0}) 
    fig.update_coloraxes( # edit legend
        colorbar=dict(
            title=dict(text="Period Poverty<br>Index", 
                       font=dict(size=LT_SIZE)),
            tickfont=dict(size=L_SIZE),
            orientation='v', 
            len=0.8,
            thickness=15,
            ypad=8,
            yanchor='middle'))
    fig.update_traces( # polygon border
        marker_line_width=0.8, marker_line_color='white')

    return fig

fig_idx = create_idx_maps(df, census_tracts, 9.4, 41.8227, -87.6014)

# --------- filtered census tract pp index maps -------------

# we can just change map zoom and coordinates?

fig_idx_med = create_idx_maps(df, census_tracts, 11, 41.76113, -87.61485)


# ---------------- community centers map --------------------

joined = gpd.read_file("ppindex/src/comm_centers_neighborhoods.geojson")
joined["lat"] = joined.geometry.y
joined["lon"] = joined.geometry.x

def create_cc_maps(df, lat, lon):
    '''
    this function creates the community centers map

    input: df (pandas dataframe)
           lat (int) latitude 
           long (int) longitude 
    output: scatter map (plotly express class)
    '''

    fig_cc = px.scatter_mapbox(df, 
                        lat=lat, 
                        lon=lon, 
                        hover_name="Community Center",
                        hover_data={'Neighborhood': True, 'lat':False, 
                                    'lon':False},
                        opacity=0.5,
                        color="Category",
                        color_discrete_sequence=px.colors.qualitative.Bold,
                        mapbox_style="carto-positron")
    
    fig_cc.update_layout(
        title_x=0.5, 
        font=dict(family=L_FONT,
                  size=L_SIZE+1),
        margin={"r":0,"t":0,"l":0,"b":0})

    return fig_cc

# --- neighborhood dropdown options ---

options = [{'label': neighborhood, 
'value': neighborhood} for neighborhood in sorted(joined['Neighborhood'\
].unique())]
options[0]['label'] = 'All'
options[0]['value'] = 'All'

fig_cc = create_cc_maps(joined, 'lat', 'lon')

# --------------------------- html page layout here ----------------------------

app.layout = dbc.Container([
    # header
    dbc.Row([
        dbc.Col([
            html.Br(), 
            html.H1('Understanding Period Poverty in Chicago', 
                    style={'text-align':'center'}),
            html.P('Betty Fang, Diamon Dunlap, Ivanna Rodríguez, Jimena Salinas', 
            style={'text-align':'center'}),
        ], width=12) 
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
            pariatur. Excepteur sint occaecat cupidatat non proident, sunt in \
            culpa qui officia deserunt mollit anim id est laborum. \
            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris \
            nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in \
            reprehenderit in voluptate velit esse cillum dolore eu fugiat null', 
            html.Br(), 'now I am adding a new line break but does this text ']),
        ], width=12) # 12 is maximum you can take
    ], align='end'),

    # index methodology (?)

    # index map
    dbc.Row([
        dbc.Col([

            html.H3('Period Poverty by Census Tract', 
            style={'text-align':'center'}),
            
            dcc.Graph(
                id='map-idx',
                figure = fig_idx)
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
        
        html.Br(),
        html.H3('Community Based Services and Commercial Retailers', 
        style={'text-align':'center'}),

        dbc.Col([
            html.Label(['Neighborhood:'], style={"margin-top":0}),
            dcc.Dropdown(
                id='neighborhood_dropdown',
                options=options,
                value=options[0]['value'],
                style={"margin-top":7}
                )
        ], width=2, align='start'),

        dbc.Col([
            dcc.Graph(
                id='map-cc',
                figure = fig_cc
                )
        ], width=10)

    ], align='center'),

    # community centers text
    dbc.Row([
        dbc.Col([
            html.Br(), 
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
            html.Br(), 'now I am adding a new line break but does this text ']),
        ], width=12) 
    ], align='end'),

    # three filtered maps w highlighted areas
    dbc.Row([
        html.Br(),
        dbc.Col([
            html.P(['Lorem ipsum dolor sit amet, consectetur adipiscing elit, \
            sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. \
            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris \
            nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in \
            reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla\
            pariatur. Excepteur sint occaecat cupidatat non proident, sunt in\
            culpa qui officia deserunt mollit anim id est laborum. \
            Lorem ipsum dolor sit amet, consectetur adipiscing elit'])
        ], width=6),
        
        dbc.Col([

            html.H3('Radius Map Will Go Here(ish)', 
            style={'text-align':'center'}),

            dcc.Graph(
                id='map-idx-med',
                figure = fig_idx_med)
        ], width=6)
    ], align='center')

])

# ---------------------------- app callback --------------------------------

@app.callback(
    Output('map-cc', 'figure'),
    Input('neighborhood_dropdown', 'value')
)
def update_map(neighborhood_dropdown):
    # Find the center and zoom level for the selected neighborhood

    if neighborhood_dropdown == "All":
        zoom_level = 9.4
        fig = create_cc_maps(joined, "lat", "lon")
        # Update the layout of the map with the new center and zoom level
        fig['layout']['mapbox']['center'] = {'lat': 41.8227, 'lon': -87.6014}
        fig['layout']['mapbox']['zoom'] = zoom_level
    else:
        center_lat = joined[joined['Neighborhood'] == neighborhood_dropdown\
        ]['lat'].mean()
        center_lon = joined[joined['Neighborhood'] == neighborhood_dropdown\
        ]['lon'].mean()
        zoom_level = 12
        fig = create_cc_maps(joined, "lat", "lon")
        # Update the layout of the map with the new center and zoom level
        fig['layout']['mapbox']['center'] = {'lat': center_lat, 
                                             'lon': center_lon}
        fig['layout']['mapbox']['zoom'] = zoom_level

    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
