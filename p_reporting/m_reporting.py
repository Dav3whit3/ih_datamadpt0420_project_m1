import pandas as pd
import plotly.graph_objects as go

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from p_analysis import m_analysis as man


# reporting functions
def dash_report(df):
    df = man.analyze(df)
    app = dash.Dash(__name__)

    app.layout = html.Div([

        html.H1("Challenge 1", style={'text-align': 'center'}),

        html.Label('Job Title'),
        dcc.Dropdown(
            id='select_job',
            options=[
                {'label': elem, 'value': elem} for elem in df['Job_title'].unique()
            ],
            value='geographic information systems data administrator gis data administrator'
        ),
        html.Br(),

        html.Label('Country'),
        dcc.Dropdown(
            id='select_country',
            options=[
                {'label': elem, 'value': elem} for elem in df['Country'].unique()
            ],
            value='Spain'
        ),
        html.Br(),

        html.Label('Age Group'),
        dcc.Dropdown(
            id='select_age_group',
            options=[
                {'label': elem, 'value': elem} for elem in df['Age_group'].unique()
            ],
            value='14_25',
        ),

        dcc.Graph(id='my_table', figure={})

    ])

    @app.callback(
        Output(component_id='my_table', component_property='figure'),
        [Input(component_id='select_job', component_property='value'),
         Input(component_id='select_country', component_property='value'),
         Input(component_id='select_age_group', component_property='value')]
    )
    def update_graph(job_slctd, country_slctd, age_slctd):
        dff = df.copy()
        dff = dff[(dff['Job_title'] == job_slctd) & (dff['Country'] == country_slctd) & (dff['Age_group'] == age_slctd)]

        fig = go.Figure(data=[go.Table(
            header=dict(values=list(dff.columns),
                        fill_color='paleturquoise',
                        align=['left', 'center'],
                        height=40,
                        ),
            cells=dict(values=[dff.Country, dff.Age_group, dff.Job_title, dff.Quantity, dff.Percentage],
                       fill_color='lavender',
                       align=['left', 'center'],
                       height=30,
                       ))
        ])
        fig.update_layout()

        return fig

    return app.run_server(debug=True, use_reloader=False)


def export(csv, args):
    result = csv
    pais = "todos"
    opcion = input("Do you want to filter a specific country in the final DataFrame? (y/n)")
    print("...")
    while opcion != "y" and opcion != "n":
        opcion = input("Wrong answer my guy! Pick y or n")
    if opcion == "y":
        pais = input("Ok then! Which country?")
        print("...")
        result = man.country_filter(pais, result)
        print(f"Okay! Your DataFrame will be filtered by {pais}")

    print(f"Your final DataFrame has been saved at {args} as {pais}.csv")
    print("...")

    return result.to_csv(f'{args}{pais}.csv')


