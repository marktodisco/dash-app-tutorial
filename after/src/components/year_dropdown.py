from dash import html, dcc

from src import default_options

__all__ = ["year_dropdown"]


year_dropdown = html.Div(
    [
        html.H6("Year"),
        dcc.Dropdown(
            id="year-dropdown",
            options=default_options.get_year_options(),
            value=default_options.get_year_values(),
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
