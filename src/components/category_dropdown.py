import src
from dash import dcc, html


def render() -> html.Div:
    transactions = src.transactions.load_transaction_data()
    return html.Div(
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
    )
