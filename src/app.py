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

census_tracts = gpd.read_file("boundaries_census_tracts_2010.geojson")
df = pd.read_json("index_w_neigh_names.json")

# figure
fig_idx = px.choropleth_mapbox(df, geojson = census_tracts, 
                            locations = "tract", color="pp_index", 
                            color_continuous_scale="amp", range_color=(0, 20.7), 
                            featureidkey="properties.tractce10",
                            mapbox_style="carto-positron", opacity=0.5,
                            hover_name="neighborhood_name",
                            center={"lat": 41.8227, "lon": -87.6014}, zoom=9.4)
fig_idx.update_geos(fitbounds="locations", visible=False)
fig_idx.update_layout(title_text='Period Poverty Index by Census Tract', title_x=0.5,
    margin={"r":0,"t":40,"l":0,"b":0})
fig_idx.update_traces(marker_line_width=1, marker_line_color='white')

# fig_idx.update_layout({
#     'updatemenus': [{
#         'buttons': [
#             {
#                 'args': [{'mapbox.zoom':12, 'mapbox.center.lat':census_tracts[census_tracts['neighborhood_name'] == neighborhood]['lat'].iloc[0],
#                           'mapbox.center.lon': census_tracts[census_tracts['neighborhood_name'] == neighborhood]['lon'].iloc[0]}],
#                 'label': neighborhood,
#                 'method': 'relayout'
#             } for neighborhood in census_tracts['neighborhood_name'].unique()
#         ],
#         'direction': 'down',
#         'showactive': True,
#         'x': 0.01,
#         'y': 0.95
#     }]
# })

# ---------------- community centers map --------------------

joined = gpd.read_file("comm_centers_neighborhoods.geojson")

fig_cc = px.scatter_mapbox(joined, 
                        lat=joined.geometry.y, 
                        lon=joined.geometry.x, 
                        zoom=9,
                        hover_name="Community Center",
                        hover_data=['Neighborhood'],
                        # hover_data={'Neighborhood': True, 'lat':False, 'lon':False},
                        opacity=0.5,
                        color="Type",
                        mapbox_style="carto-positron")
fig_cc.update_layout(title_text='Women and Girls Community Centers in Chicago', 
    title_x=0.5, margin={"r":0,"t":40,"l":0,"b":0})
fig_cc.update_layout({
    'updatemenus': [{
        'buttons': [
            {
                'args': [{'mapbox.zoom':12, 'mapbox.center.lat':joined[joined['Neighborhood'] == neighborhood]['lat'].iloc[0],
                          'mapbox.center.lon': joined[joined['Neighborhood'] == neighborhood]['lon'].iloc[0]}],
                'label': neighborhood,
                'method': 'relayout'
            } for neighborhood in joined['Neighborhood'].unique()
        ],
        'direction': 'down',
        'showactive': True,
        'x': 0.01,
        'y': 0.95
    }]
})

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
        dbc.Col([
            dcc.Graph(
                id='map-cc',
                figure = fig_cc)
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
