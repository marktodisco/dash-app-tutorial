from dash import html, dcc

from src import default_options

__all__ = ["category_dropdown"]


category_dropdown = html.Div(
    children=[
        html.H6("Category"),
        dcc.Dropdown(
            id="category-dropdown",
            options=default_options.get_category_options(),
            value=default_options.get_category_values(),
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
