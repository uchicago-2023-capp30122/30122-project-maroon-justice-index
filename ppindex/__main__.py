import dash
from dash import html
import dash_bootstrap_components as dbc
from .src.app import app

if __name__ == '__main__':
    app.run_server(debug=True)