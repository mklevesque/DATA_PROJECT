# -*- coding: utf-8 -*-
"""
Created on Mon May  2 14:44:30 2022

@author: cazen
"""


import dash_bootstrap_components as dbc
from dash import html, Dash, html, dcc, Input, Output
import pandas as pd
import requests
import plotly.express as px
app = Dash(__name__)

df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2]
})

fig = px.bar(df, x="Fruit", y="Amount", barmode="group")

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content'),
])

display_stat = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for your data.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

not_found_page = html.Div([
    dcc.Location(id='url', refresh=False),
    html.H1(children="nothing")
])

index_page = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Form([
        dcc.Input(
            type="text",
            name="something",
        ),
        html.Button('Submit', id='idSubmit'),
    ], action="/recipe_profiling"),
    html.Div(id="output")
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname'),
              Input('url', 'search')])
def display_page(pathname, search):
    if pathname == '/':
        return index_page
    elif pathname == "/recipe_profiling":
        if search != "":
            print(search.split("=")[1])
            result = search.split("=")[1]
            response = requests.get(f"http://127.0.0.1:5000/get_recipe/{result}")
        return display_stat
    else:
         return not_found_page
     
# app.layout = html.Div(children=[
#     dbc.Form(
#         dbc.Row(
#             [
#                 dbc.Label("Recette", width="auto"),
#                 dbc.Col(
#                     dbc.Input(type="text", id ="url_recipe", placeholder="Lien de la recette"),
#                     className="me-3",
#                 ),
#                 dbc.Col(dbc.Button("Envoyer", id="get_url",color="primary"), width="auto"),
#             ],
#             className="g-2",
#         ), action="http:/localhost:5000/get_result", method="POST"
#     )
# ])

if __name__ == '__main__':
    app.run_server(debug=True)