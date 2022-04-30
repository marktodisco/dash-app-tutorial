import argparse
import sys
from argparse import ArgumentParser
from dataclasses import dataclass
from typing import Any, List

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


@app.callback(
    [Output("month-dropdown", "value"), Output("select-all-month-button-clicks", "data")],
    [
        Input("year-dropdown", "value"),
        Input("month-dropdown", "value"),
        Input("select-all-month-button", "n_clicks"),
        Input("select-all-month-button-clicks", "data"),
    ],
)
def select_all_months(
    years: list[int], months: list[str], n_clicks: int, previous_n_clicks: int
) -> tuple[list[str], int]:
    filtered_transactions = transactions.query(f"Year == {years}")
    clicked = n_clicks <= previous_n_clicks
    new_months = months if clicked else list(filtered_transactions.dropna()["Month"].unique())
    return sorted(new_months), n_clicks


@app.callback(
    Output("category-dropdown", "value"),
    [
        Input("year-dropdown", "value"),
        Input("month-dropdown", "value"),
        Input("select-all-category-button", "n_clicks"),
    ],
)
def select_all_categories(year: list[int], month: list[int], _: list[int]) -> list[str]:
    categories: list[str] = list(
        transactions.dropna()
        .query(f"Year == {year}")
        .query(f"Month == {month}")
        .loc[:, "Category"]
        .unique()
    )
    return sorted(categories)


@app.callback(
    Output("budget-pivot-table-records", "data"),
    [
        Input("year-dropdown", "value"),
        Input("month-dropdown", "value"),
        Input("category-dropdown", "value"),
    ],
)
def filter_budget_records(
    years: List[int], months: List[str], categories: List[str]
) -> BudgetRecordsAlias:
    def filter_transactions(years: List[int], months: List[str], categories: List[str]):
        transactions = (
            Transactions(load_transaction_data())
            .filter(col_name="Year", values=years)
            .filter(col_name="Month", values=months)
            .filter(col_name="Category", values=categories)
        )
        transactions_df = transactions.to_data_frame().drop(columns=["Index"])
        return transactions_df

    def create_pivot_table(transactions: pd.DataFrame) -> BudgetDataFrame:
        transactions_pivot_table: BudgetDataFrame = transactions.pivot_table(  # type: ignore
            values=["Amount"],
            index=["Category"],
            aggfunc="sum",
            fill_value=0,
            dropna=False,
        ).reset_index()
        return transactions_pivot_table

    def drop_bad_transactions(transactions_pivot_table: BudgetDataFrame):
        _transactions_pivot_table = transactions_pivot_table.copy()
        for idx in ["Income", "Ignore"]:
            if idx in _transactions_pivot_table.Category:
                _transactions_pivot_table.drop(index=idx, inplace=True)
        return _transactions_pivot_table

    transactions = filter_transactions(years, months, categories)
    transactions = create_pivot_table(transactions)
    drop_bad_transactions(transactions)
    return transactions.to_dict("records")  # type: ignore


if __name__ == "__main__":
    app.run_server(debug=True)
