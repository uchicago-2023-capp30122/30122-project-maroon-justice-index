# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
import numpy as np

external_stylesheets = [
    "https://fonts.googleapis.com/css2?family=Roboto:wght@300&display=swap"
]

app = Dash(__name__, external_stylesheets=external_stylesheets)

# ------------------ data and map here --------------------------------

neighborhoods = "https://raw.githubusercontent.com/blackmad/neighborhoods/master/chicago.geojson"

# generate some data for each region defined in geojson...
df = pd.DataFrame(
    {"fips": range(1, 77, 1), "unemp": np.random.uniform(0.4, 10.4, 76)}
)

fig = px.choropleth_mapbox(df, geojson = neighborhoods, 
                           locations = "fips",
                           color="unemp",
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

app.layout = html.Div(children=[
    html.H1('A Map of Chicago Neighborhoods', style={'text-align':'center'}),
    html.P('This is a paragraph introducing stuff\nhow do i start a new line'),

    html.Div('''
        With randomly generated data
    '''),

    dcc.Graph(
        id='graph',
        figure = fig
    )

], style={'marginLeft': 60, 'marginTop': 60})




if __name__ == '__main__':
    app.run_server(debug=True)
