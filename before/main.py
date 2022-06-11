from datetime import datetime

import dash_bootstrap_components as dbc
from dash import Dash, dcc, html

from src import defaults
from src.callbacks import register_callbacks
from src.schema import TransactionsSchema
from src.transactions import load_transaction_data

transactions = load_transaction_data()
years = sorted(transactions.loc[:, TransactionsSchema.Year].unique())
months = sorted(transactions.loc[:, TransactionsSchema.Month].unique())

now = datetime.now()
current_year = now.year
current_month = now.strftime("%m-%b")

year_filter = {str(year): False for year in years if year != current_year}
month_filter = {str(month): False for month in months if month != current_month}


app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, "https://codepen.io/chriddyp/pen/bWLwgP.css"],
)

app.title = "Financial Dashboard"

app.layout = html.Div(
    className="app-div",
    children=[
        html.H1("Financial Dashboard"),
        html.Hr(),
        html.Div(
            children=[
                html.H6("Year"),
                dcc.Dropdown(
                    id="year-dropdown",
                    options=defaults.get_year_options(transactions),
                    value=defaults.get_year_values(),
                    multi=True,
                ),
                html.Button(
                    className="dropdown-button",
                    children=["Select All"],
                    id="select-all-year-button",
                    n_clicks=0,
                ),
            ]
        ),
        html.Div(
            children=[
                html.H6("Month"),
                dcc.Dropdown(
                    id="month-dropdown",
                    options=defaults.get_month_options(transactions),
                    value=defaults.get_month_values(),
                    multi=True,
                ),
                html.Button(
                    className="dropdown-button",
                    children=["Select All"],
                    id="select-all-month-button",
                    n_clicks=0,
                ),
            ]
        ),
        html.Div(
            children=[
                html.H6("Category"),
                dcc.Dropdown(
                    id="category-dropdown",
                    options=defaults.get_category_options(transactions),
                    value=defaults.get_category_values(transactions),
                    multi=True,
                ),
                html.Button(
                    className="dropdown-button",
                    children=["Select All"],
                    id="select-all-category-button",
                    n_clicks=0,
                ),
            ],
        ),
        html.Div(id="pie-chart"),
        dcc.Store(id="filtered-transaction-records"),
        dcc.Store(id="budget-pivot-table-records"),
        dcc.Store(id="select-all-year-button-clicks", data=0),
        dcc.Store(id="select-all-month-button-clicks", data=0),
        dcc.Store(id="select-all-category-button-clicks", data=0),
    ],
)


register_callbacks(app)


if __name__ == "__main__":
    app.run_server(debug=True)
