from dash import dcc, html

import src


def create_layout() -> html.Div:
    transactions = src.transactions.load_transaction_data()
    return html.Div(
        className="app-div",
        children=[
            html.H1("Financial Dashboard"),
            html.Hr(),
            html.Div(
                children=[
                    html.H6("Year"),
                    dcc.Dropdown(
                        id="year-dropdown",
                        options=src.defaults.get_year_options(transactions),
                        value=src.defaults.get_year_values(),
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
                        options=src.defaults.get_month_options(transactions),
                        value=src.defaults.get_month_values(),
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
                        options=src.defaults.get_category_options(transactions),
                        value=src.defaults.get_category_values(transactions),
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
