from dash import dcc, html

import src


def create_layout() -> html.Div:
    return html.Div(
        className="app-div",
        children=[
            html.H1("Financial Dashboard"),
            html.Hr(),
            src.components.year_dropdown.render(),
            src.components.month_dropdown.render(),
            src.components.category_dropdown.render(),
            html.Div(id="pie-chart"),
            dcc.Store(id="filtered-transaction-records"),
            dcc.Store(id="budget-pivot-table-records"),
            dcc.Store(id="select-all-year-button-clicks", data=0),
            dcc.Store(id="select-all-month-button-clicks", data=0),
            dcc.Store(id="select-all-category-button-clicks", data=0),
        ],
    )
