import src
from dash import dcc, html


def render() -> html.Div:
    return html.Div(
        children=[
            html.H6("Year"),
            dcc.Dropdown(
                id="year-dropdown",
                options=src.defaults.get_year_options(src.transactions.load_transaction_data()),
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
    )
