# -*- coding: utf-8 -*-
"""
Created on Mon May  2 14:44:30 2022

@author: cazen
"""

import dash_bootstrap_components as dbc
from dash import html

form = dbc.Form(
    dbc.Row(
        [
            dbc.Label("Recette", width="auto"),
            dbc.Col(
                dbc.Input(type="text", placeholder="Lien de la recette"),
                className="me-3",
            ),
            dbc.Col(dbc.Button("Submit", color="primary"), width="auto"),
        ],
        className="g-2",
    )
)