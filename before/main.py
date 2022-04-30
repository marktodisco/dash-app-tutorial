import argparse
import sys
from argparse import ArgumentParser
from dataclasses import dataclass
from typing import List

import dash_bootstrap_components as dbc
import pandas as pd
from dash import Dash, dcc, html
from dash.dependencies import Input, Output

from src.callbacks import register_callbacks
from src.components import (
    category_dropdown,
    month_dropdown,
    pivot_table,
    tabs,
    year_dropdown,
)
from src.data import Transactions, load_transaction_data
from src.typing.aliases import BudgetRecordsAlias
from src.typing.classes import BudgetDataFrame

transactions = load_transaction_data()

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, "https://codepen.io/chriddyp/pen/bWLwgP.css"],
)

app.title = "Financial Dashboard"

app.layout = html.Div(
    className="app-div",
    children=[
        html.H1("Financial Dashboard"),
        year_dropdown,
        month_dropdown,
        category_dropdown,
        # tabs,
        # html.Hr(),
        # html.H3("Transactions"),
        # pivot_table,
        dcc.Store(id="filtered-transaction-records"),
        dcc.Store(id="budget-pivot-table-records"),
        dcc.Store(id="select-all-year-button-clicks", data=0),
        dcc.Store(id="select-all-month-button-clicks", data=0),
        dcc.Store(id="select-all-category-button-clicks", data=0),
    ],
)

register_callbacks(app)


@app.callback(
    [Output("year-dropdown", "value"), Output("select-all-year-button-clicks", "data")],
    [
        Input("year-dropdown", "value"),
        Input("select-all-year-button", "n_clicks"),
        Input("select-all-year-button-clicks", "data"),
    ],
)
def select_all_years(
    years: list[int], n_clicks: int, previous_n_clicks: int
) -> tuple[list[int], int]:
    clicked = n_clicks <= previous_n_clicks
    new_years = years if clicked else list(transactions.dropna()["Year"].unique())
    return sorted(new_years), n_clicks


if __name__ == "__main__":
    app.run_server(debug=True)
