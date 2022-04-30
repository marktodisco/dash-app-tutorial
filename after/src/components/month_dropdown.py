from dash import html, dcc

from src import default_options

__all__ = ["month_dropdown"]


month_dropdown = html.Div(
    [
        html.H6("Month"),
        dcc.Dropdown(
            id="month-dropdown",
            options=default_options.get_month_options(),
            value=default_options.get_month_values(),
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
