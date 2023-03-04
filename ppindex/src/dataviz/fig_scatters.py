'''
CAPP 122: Project Maroon Justice Index
Jimena Salinas
Code for creating a scatter plot that
shows the relationship between period poverty
index values and the number of community 
resource centers and retailers, and a scatter
for showing the relationship between income,
number of eligible women, and index.
'''

import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.colors as colors

import pandas as pd
import pandas as pd

import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.colors as colors


def create_index_centers_scatter(font_family, font_size):
    """
    Creates a scatter plot of the Period Poverty Index (pp_index) vs. 
    the number of community-based services and commercial
    retailers for each US Census tract in Illinois.

    Returns:
        - fig (plotly figure object): a Plotly figure object 
        containing the scatter plot.
    """
    pp_dta = pd.read_json("data/index_data_for_scatter.json")

    # Custom colorscale with shades of dark wine red
    custom_reds = colors.make_colorscale(
        ['#FFEEEE', '#E27B91', '#C83652', '#722f37'])

    # Create a scatter plot of pp_index vs. number_of_centers,
    # where each point represents a tract
    scatter = go.Scatter(x=pp_dta['number_of_centers'], y=pp_dta['pp_index'],
                         mode='markers',
                         marker=dict(color=pp_dta['pp_index'],
                                     colorscale=custom_reds,
                                     reversescale=False,
                                     sizemode='diameter',
                                     sizeref=0.1,
                                     size=6,
                                     opacity=1,
                                     colorbar=dict(title='Period Poverty Index')),
                         text=pp_dta['neighborhood_name'])

    fig = make_subplots(rows=1, cols=1, specs=[[{}]], shared_xaxes=True,
                        shared_yaxes=False, horizontal_spacing=0.1)

    fig.add_trace(scatter, row=1, col=1)

    # y-axis title
    fig.update_yaxes(title_text='Period Poverty Index',
                     row=1, col=1, range=[0.05, None])

    # x-axis title
    fig.update_xaxes(
        title_text='Number of Community-Based Services and Commercial Retailers', row=1, col=1)

    # make the background white
    fig.update_layout(plot_bgcolor='white')

    return fig


def create_income_population_scatter(font_family, font_size):
    """
    Creates a scatter plot of total eligible women vs. average disposable 
    income per month, filtered to show only income per month of 2,900 or less.

    Parameters:
    - font_family (str): font family for plot titles and axis labels
    - font_size (int): font size for plot titles and axis labels

    Returns:
    - fig (plotly figure object): A Plotly Figure object containing the scatter plot.
    """
    pp_dta = pd.read_json("data/index_data_for_scatter.json")

    # Custom colorscale with shades of dark wine red
    custom_reds = colors.make_colorscale(
        ['#FFEEEE', '#E27B91', '#C83652', '#722f37'])

    # Filter the data to show only income per month of 2,900 or less
    filtered_data = pp_dta[pp_dta['avg_disposable_income_per_month'] <= 2900]

    # Create a scatter plot of total_eligible_women vs.
    # avg_disposable_income_per_month, where each point represents a tract
    scatter = go.Scatter(x=filtered_data['avg_disposable_income_per_month'],
                         y=filtered_data['total_eligible_women'],
                         mode='markers',
                         marker=dict(color=filtered_data['pp_index'],
                                     colorscale=custom_reds,
                                     reversescale=False,
                                     sizemode='diameter',
                                     sizeref=0.1,
                                     size=filtered_data['pp_index']*6,
                                     opacity=0.6,
                                     colorbar=dict(title='Period Poverty Index')),
                         text=filtered_data['neighborhood_name'])

    fig = make_subplots(rows=1, cols=1, specs=[[{}]], shared_xaxes=True,
                        shared_yaxes=False, horizontal_spacing=0.1)

    fig.add_trace(scatter, row=1, col=1)

    # y-axis title
    fig.update_yaxes(title_text='Total Eligible Women', row=1, col=1, 
                     title_font=dict(family=font_family, size=font_size))

    # x-axis title
    fig.update_xaxes(title_text='Average Disposable Income per Month', row=1, col=1, 
                     title_font=dict(family=font_family, size=font_size))

    # plot title and background color
    fig.update_layout(title='Total Eligible Women vs. Average Disposable Income per Month',
                      plot_bgcolor='white', 
                      font=dict(family=font_family, size=font_size))

    return fig
