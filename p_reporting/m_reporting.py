import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output


# reporting functions
def dash_report(df):

    app = dash.Dash(__name__)
    fig = go.Figure(data=[go.Table(
        header=dict(values=list(df.columns),
                    fill_color='paleturquoise',
                    align=['left', 'center'],
                    height=40,
                    ),
        cells=dict(values=[df.Country, df.Age_group, df.Job_title, df.Quantity, df.Percentage],
                   fill_color='lavender',
                   align=['left', 'center'],
                   height=30,
                   ))
    ])

    app.layout = html.Div([

        html.H1("Challenge 1", style={'text-align': 'center'}),

        dcc.Dropdown(
            id='demo-dropdown',
            options=[
                {'label': elem, 'value': elem} for elem in df['Country'].unique()
            ],
            value='Spain'
        ),

        html.Div(id='dd-output-container'),

        dcc.Graph(figure=fig)

    ])

    return app.run_server(debug=True)#, use_reloader=False)

'''
def visualize_barplot(df,title):
    fig, ax = plt.subplots(figsize=(15,8))
    chart = sns.barplot(data=df, x='Make', y='Combined MPG')
    plt.title(title + "\n", fontsize=16)
    return chart

def visualize_lineplot(df,title):
    fig, ax = plt.subplots(figsize=(15,8))
    chart = sns.lineplot(data=df, x='Make', y='Combined MPG')
    plt.title(title + "\n", fontsize=16)
    return chart


def plotting_function(df,title,args):
    fig, ax = plt.subplots(figsize=(16,8))
    plt.title(title + "\n", fontsize=16)
    if args.bar == True:
        sns.barplot(data=df, x='Make', y='Combined MPG')
        return fig
    elif args.line == True:
        sns.lineplot(data=df, x='Make', y='Combined MPG')
        return fig

def save_viz(fig,title):
    fig.savefig('./data/results/' + title + '.png')

"""