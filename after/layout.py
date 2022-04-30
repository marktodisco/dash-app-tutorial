from dash import dcc, html

from src.components import (
    category_dropdown,
    month_dropdown,
    pivot_table,
    tabs,
    year_dropdown,
)

layout = html.Div(
    className="app-div",
    children=[
        html.H1("Financial Dashboard"),
        html.Hr(),
        html.H3("Monthly Expenses"),
        year_dropdown,
        month_dropdown,
        category_dropdown,
        tabs,
        html.Hr(),
        html.H3("Transactions"),
        pivot_table,
        dcc.Store(id="filtered-transaction-records"),
        dcc.Store(id="budget-pivot-table-records"),
        dcc.Store(id="select-all-year-button-clicks", data=0),
        dcc.Store(id="select-all-month-button-clicks", data=0),
        dcc.Store(id="select-all-category-button-clicks", data=0),
    ],
)
