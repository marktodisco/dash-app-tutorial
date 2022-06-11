import src
from dash import dcc, html


def render() -> html.Div:
    return html.Div(
        children=[
            html.H6("Month"),
            dcc.Dropdown(
                id="month-dropdown",
                options=src.defaults.get_month_options(src.transactions.load_transaction_data()),
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
    )
