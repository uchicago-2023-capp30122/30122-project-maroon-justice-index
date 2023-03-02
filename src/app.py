# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import geopandas as gpd
import numpy as np

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# ----------------------- data and maps here -----------------------------------

# --------- census tract pp index map ----------------

census_tracts = gpd.read_file("boundaries_census_tracts_2010.geojson")
df = pd.read_json("index_w_neigh_names.json")

dd_list = df.neighborhood_name.dropna().unique()

def create_idx_maps(df, gdf, zoom, lat, lon):

    fig = px.choropleth_mapbox(
        df, 
        geojson = census_tracts, 
        locations = "tract", 
        featureidkey="properties.tractce10",
        color="pp_index", color_continuous_scale="amp", range_color=(0, 20.7), 
        mapbox_style="carto-positron", opacity=0.5,
        hover_name="neighborhood_name",
        center={"lat": lat, "lon": lon}, zoom=zoom)

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(
        title_text='Period Poverty Index by Census Tract', 
        # coloraxis_showscales=False,
        title_x=0.5, 
        margin={"r":0,"t":40,"l":0,"b":0}) 
    fig.update_coloraxes( # edit legend
        colorbar=dict(
            title="Period<br>Poverty<br>Index",
            orientation='v', 
            len=0.8,
            thickness=10,
            ypad = 8,
            yanchor='middle'))
    fig.update_traces( # polygon border
        marker_line_width=1, marker_line_color='white')


    return fig

fig_idx = create_idx_maps(df, census_tracts, 9.4, 41.8227, -87.6014)

# --------- filtered census tract pp index maps -------------

# we can just change map zoom and coordinates?
fig_idx_south = create_idx_maps(df, census_tracts, 11, 41.6922572, -87.5583785)
fig_idx_med = create_idx_maps(df, census_tracts, 11, 41.76113, -87.61485)
fig_idx_north = create_idx_maps(df, census_tracts, 11, 41.8810, -87.7012)

# ---------------- community centers map --------------------

joined = gpd.read_file("comm_centers_neighborhoods.geojson")
joined["lat"] = joined.geometry.y
joined["lon"] = joined.geometry.x

def create_cc_maps(df, zoom):
    fig_cc = px.scatter_mapbox(df, 
                        lat="lat", 
                        lon="lon", 
                        zoom=zoom,
                        hover_name="Community Center",
                        # hover_data=['Neighborhood'],
                        hover_data={'Neighborhood': True, 'lat':False, 'lon':False},
                        opacity=0.5,
                        color="Category",
                        color_discrete_sequence=px.colors.qualitative.Bold,
                        mapbox_style="carto-positron")
    
    fig_cc.update_layout(
        title_text='Women and Girls Community Centers in Chicago', title_x=0.5, 
        margin={"r":0,"t":40,"l":0,"b":0})

    fig_cc.update_layout({
        'updatemenus': [{
            'buttons': [
                {
                    'args': [{'mapbox.zoom':12, 'mapbox.center.lat':df[df['Neighborhood'] == neighborhood]['lat'].iloc[0],
                            'mapbox.center.lon': df[df['Neighborhood'] == neighborhood]['lon'].iloc[0]}],
                    'label': neighborhood,
                    'method': 'relayout'
                } for neighborhood in df['Neighborhood'].unique()
            ],
            'direction': 'down',
            'showactive': True,
            'x': 0.01,
            'y': 0.95
        }]
    })

    return fig_cc

fig_cc = create_cc_maps(joined, 10)

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
            dcc.Dropdown(
                id='dropdown',
                options=[{'label': i, 'value': i} for i in dd_list],
                # value=dd_list['neighborhood_name'].unique()[0],
                placeholder="Please select..",
                searchable=True)
        ], width=2, align='start'),

        dbc.Col([
            dcc.Graph(
                id='map-idx',
                figure = fig_idx)
        ], width=10)

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
                id='map-cc',
                figure = fig_cc
                )
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
    ], align='end'),

    # three filtered maps w highlighted areas
    dbc.Row([
        html.Br(),
        dbc.Col([
            dcc.Graph(
                id='map-idx-south',
                figure = fig_idx_south)
        ], width=6),
        
        dbc.Col([
            dcc.Graph(
                id='map-idx-med',
                figure = fig_idx_med)
        ], width=6)
    ], align='center')

])

# ---------------------------- app callback ------------------------------

@app.callback(
    Output("map-idx", "figure"),
    Input("dropdown","value"))

def display_index_map(selected_neighborhood):
    flt_df = df[df['neighborhood_name'] == selected_neighborhood]
    lat = flt_df.neigh_lat.drop_duplicates()
    lon = flt_df.neigh_lon.drop_duplicates()

    return create_idx_maps(df, census_tracts, 13, lat.values[0], lon.values[0])
    

if __name__ == '__main__':
    app.run_server(debug=True)
