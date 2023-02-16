# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import numpy as np

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# ------------------ data and map here --------------------------------

neighborhoods = "https://raw.githubusercontent.com/blackmad/neighborhoods/master/chicago.geojson"

# generate some data for each region defined in geojson...
df = pd.DataFrame(
    {"neighborhood": range(1, 77, 1), "period_pov_index": np.random.uniform(0.4, 10.4, 76)}
)

fig = px.choropleth_mapbox(df, geojson = neighborhoods, 
                           locations = "neighborhood",
                           color="period_pov_index",
                           color_continuous_scale="Viridis",
                           range_color=(0, 12),
                           featureidkey="properties.cartodb_id",
                           mapbox_style="carto-positron",
                           opacity=0.5,
                           center = {"lat": 41.8781, "lon": -87.6298},
                           zoom=9)
fig.update_geos(fitbounds="locations",visible=False)
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},)
# fig.update_traces(marker=dict(size=10, 
#                               line=dict(width=3, color='white')))
fig.show()



# ------------------ html page layout here ----------------------------

app.layout = dbc.Container([

    # header
    dbc.Row([
        dbc.Col([
            html.H1('Mapping Period Poverty in Chicago', style={'text-align':'center'}),
            html.P('Betty Fang, Diamon Dunlap, Ivanna Rodríguez, Jimena Salinas', style={'text-align':'center', 'font-style':'italic'}),
        ], width=12, align='end') # align supposed to add padding but not working
    ]),

    # intro
    dbc.Row([
        dbc.Col([
            html.P(['Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
            html.Br(), 'now I am adding a new line break but does this text appear??']),
        ], width=12) # 12 is maximum you can take
    ]),

    # index methodology (?)


    # index map
    dbc.Row([
        dbc.Col([
            dcc.Graph(
                id='graph',
                figure = fig)
        ], width=12)
    ]),

    # community centers text
    dbc.Row([
        dbc.Col([
            html.P(['Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.',
            ])
        ], width = 12, align='end') # how do u add padding...?
    ])

    # community centers map

], className="pad-row")



if __name__ == '__main__':
    app.run_server(debug=True)
