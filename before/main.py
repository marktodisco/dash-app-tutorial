from datetime import datetime
from typing import Any, List

import dash_bootstrap_components as dbc
import pandas as pd
import pandera as pa
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from dash_pivottable import PivotTable

from src import default_options
from src.app_utils import generate_random_id
from src.data import (
    Transactions,
    create_date_check_func,
    load_budget_data,
    load_transaction_data,
)

transactions_schema = pa.DataFrameSchema(
    columns={
        "Date": pa.Column(str, pa.Check(create_date_check_func("%m/%d/%Y"))),
        # "Year": pa.Column(str, pa.Check(create_date_check_func("%Y"))),
        "Month": pa.Column(str, pa.Check(create_date_check_func("%m-%b"))),
        "Amount": pa.Column(float),
        "Label": pa.Column(str),
        "Account": pa.Column(str),
        "Description": pa.Column(str),
        "Category": pa.Column(str, nullable=True),
    }
)
transactions = transactions_schema.validate(load_transaction_data())
planned_budget = load_budget_data()

years = sorted(transactions["Year"].unique())
months = sorted(transactions["Month"].unique())

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
                    options=default_options.get_year_options(transactions),
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
        ),
        html.Div(
            children=[
                html.H6("Month"),
                dcc.Dropdown(
                    id="month-dropdown",
                    options=default_options.get_month_options(transactions),
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
        ),
        html.Div(
            children=[
                html.H6("Category"),
                dcc.Dropdown(
                    id="category-dropdown",
                    options=default_options.get_category_options(transactions),
                    value=default_options.get_category_values(transactions),
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
        html.Div(id="bar-chart"),
        html.Hr(),
        html.H3("Transactions Pivot Table"),
        "The pivot table is not controlled by the drop down menus above.",
        html.Div(
            id="div-pivot-table",
            children=PivotTable(
                # A bug with a previous version of `dash_pivottable.PivotTable` required creating a
                # random `id`. I think this issue has since been solved, but we may want to keep
                # the workaround for backwards compatability.
                id=generate_random_id(),
                data=transactions.to_dict("records"),
                rows=["Category"],
                cols=["Year", "Month"],
                vals=["Amount"],
                rendererName="table",
                aggregatorName="Sum",
                valueFilter={"Year": year_filter, "Month": month_filter},
            ),
        ),
        dcc.Store(id="filtered-transaction-records"),
        dcc.Store(id="budget-pivot-table-records"),
        dcc.Store(id="select-all-year-button-clicks", data=0),
        dcc.Store(id="select-all-month-button-clicks", data=0),
        dcc.Store(id="select-all-category-button-clicks", data=0),
    ],
)


@app.callback(
    [Output("year-dropdown", "value"), Output("select-all-year-button-clicks", "data")],
    [
        Input("year-dropdown", "value"),
        Input("select-all-year-button", "n_clicks"),
        Input("select-all-year-button-clicks", "data"),
    ],
)
def select_all_years(
    years: list[int], n_clicks: int, previous_n_clicks: int
) -> tuple[list[int], int]:
    clicked = n_clicks <= previous_n_clicks
    new_years = years if clicked else list(transactions.dropna()["Year"].unique())
    return sorted(new_years), n_clicks


@app.callback(
    [Output("month-dropdown", "value"), Output("select-all-month-button-clicks", "data")],
    [
        Input("year-dropdown", "value"),
        Input("month-dropdown", "value"),
        Input("select-all-month-button", "n_clicks"),
        Input("select-all-month-button-clicks", "data"),
    ],
)
def select_all_months(
    years: list[int], months: list[str], n_clicks: int, previous_n_clicks: int
) -> tuple[list[str], int]:
    filtered_transactions = transactions.query(f"Year == {years}")
    clicked = n_clicks <= previous_n_clicks
    new_months = months if clicked else list(filtered_transactions.dropna()["Month"].unique())
    return sorted(new_months), n_clicks


@app.callback(
    Output("category-dropdown", "value"),
    [
        Input("year-dropdown", "value"),
        Input("month-dropdown", "value"),
        Input("select-all-category-button", "n_clicks"),
    ],
)
def select_all_categories(year: list[int], month: list[int], _: list[int]) -> list[str]:
    categories: list[str] = list(
        transactions.dropna()
        .query(f"Year == {year}")
        .query(f"Month == {month}")
        .loc[:, "Category"]
        .unique()
    )
    return sorted(categories)


@app.callback(
    Output("budget-pivot-table-records", "data"),
    [
        Input("year-dropdown", "value"),
        Input("month-dropdown", "value"),
        Input("category-dropdown", "value"),
    ],
)
def filter_budget_records(
    years: List[int], months: List[str], categories: List[str]
) -> list[dict[str, Any]]:
    def filter_transactions(years: List[int], months: List[str], categories: List[str]):
        transactions = (
            Transactions(load_transaction_data())
            .filter(col_name="Year", values=years)
            .filter(col_name="Month", values=months)
            .filter(col_name="Category", values=categories)
        )
        transactions_df = transactions.to_data_frame().drop(columns=["Index"])
        return transactions_df

    def create_pivot_table(transactions: pd.DataFrame) -> pd.DataFrame:
        transactions_pivot_table: pd.DataFrame = transactions.pivot_table(  # type: ignore
            values=["Amount"],
            index=["Category"],
            aggfunc="sum",
            fill_value=0,
            dropna=False,
        ).reset_index()
        return transactions_pivot_table

    def drop_bad_transactions(transactions_pivot_table: pd.DataFrame):
        _transactions_pivot_table = transactions_pivot_table.copy()
        for idx in ["Income", "Ignore"]:
            if idx in _transactions_pivot_table.Category:
                _transactions_pivot_table.drop(index=idx, inplace=True)
        return _transactions_pivot_table

    transactions_df = filter_transactions(years, months, categories)
    budget_df = create_pivot_table(transactions_df)
    budget_df_clean = drop_bad_transactions(budget_df)
    return budget_df_clean.to_dict("records")  # type: ignore


@app.callback(Output("pie-chart", "children"), Input("budget-pivot-table-records", "data"))
def update_pie_chart(budget_records: list[dict[str, Any]]) -> dcc.Graph:
    def budget_records_to_df(budget_records: list[dict[str, Any]]) -> pd.DataFrame:
        budget = pd.DataFrame(budget_records)
        for idx, row in budget.iterrows():
            if row["Amount"] > 0:
                budget = budget.loc[budget.index != idx, :]
        budget["Amount"] = -budget["Amount"]
        budget = budget.query("Amount > 0")
        return budget

    budget = budget_records_to_df(budget_records)
    pie = go.Pie(labels=budget["Category"], values=budget["Amount"], hole=0.5)
    fig = go.Figure(data=[pie])
    fig.update_layout(margin=dict(t=40, b=0, l=0, r=0))
    fig.update_traces(hovertemplate="%{label}<br>$%{value:.2f}<extra></extra>")
    return dcc.Graph(figure=fig)


@app.callback(Output("bar-chart", "children"), Input("budget-pivot-table-records", "data"))
def update_bar_chart(budget_records: list[dict[str, Any]]) -> dcc.Graph:
    def budget_records_to_df(budget_records: list[dict[str, Any]]) -> pd.DataFrame:
        budget = pd.DataFrame(budget_records)
        for idx, row in budget.iterrows():
            if row["Amount"] > 0:
                budget = budget.loc[budget.index != idx, :]
        budget["Amount"] = -budget["Amount"]
        budget = budget.query("Amount > 0")
        return budget

    budget = budget_records_to_df(budget_records)

    budget["Percentage"] = 100 * budget["Amount"] / budget["Amount"].sum()
    budget["Percentage"] = budget["Percentage"].map(lambda x: f"{x:.2f}%")

    budget.sort_values("Amount", ascending=False, inplace=True)

    budget["Amount"] = budget["Amount"].round(2)

    fig = go.Figure(
        data=[
            go.Bar(
                x=budget["Category"],
                y=budget["Amount"],
                name="Actual Expense",
            ),
            go.Bar(
                x=planned_budget.index,
                y=planned_budget["Amount"],
                name="Planned Expense",
                visible="legendonly",
            ),
        ]
    )
    fig.update_layout(margin=dict(t=40, b=0, l=0, r=0), barmode="group")
    fig.update_traces(textposition="outside")
    return dcc.Graph(figure=fig)


if __name__ == "__main__":
    app.run_server(debug=True)
