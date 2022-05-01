from datetime import datetime
from typing import Any

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from dash_pivottable import PivotTable
from sklearn.pipeline import make_pipeline

from src import defaults, transformers
from src.random import generate_random_id
from src.schema import TransactionsSchema

transaction_preprocessing_pipeline = make_pipeline(
    transformers.CreateYearFromDate(),
    transformers.CreateMonthFromDate(),
)
raw_transactions = pd.read_csv("./data/transactions.csv")
transactions = transaction_preprocessing_pipeline.fit_transform(raw_transactions)
TransactionsSchema.validate(transactions)

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
                rows=[TransactionsSchema.Category],
                cols=[TransactionsSchema.Year, TransactionsSchema.Month],
                vals=[TransactionsSchema.Amount],
                rendererName="table",
                aggregatorName="Sum",
                valueFilter={
                    TransactionsSchema.Year: year_filter,
                    TransactionsSchema.Month: month_filter,
                },
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
    years: list[str], n_clicks: int, previous_n_clicks: int
) -> tuple[list[str], int]:
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
    years: list[int], months: list[str], categories: list[str]
) -> list[dict[str, Any]]:
    year_mask = transactions.isin(years).loc[:, TransactionsSchema.Year]
    month_mask = transactions.isin(months).loc[:, TransactionsSchema.Month]
    category_mask = transactions.isin(categories).loc[:, TransactionsSchema.Category]
    row_mask = year_mask & month_mask & category_mask
    filtered_transactions: pd.DataFrame = transactions.loc[row_mask, :]

    transactions_pivot_table = filtered_transactions.pivot_table(
        values=[TransactionsSchema.Amount],
        index=[TransactionsSchema.Category],
        aggfunc="sum",
        fill_value=0,
        dropna=False,
    ).reset_index()

    # fmt: off
    keep_rows_mask = ~(
        transactions_pivot_table
        .isin(["Income", "Ignore"])
        .loc[:, TransactionsSchema.Category]
    )
    # fmt: on
    return transactions_pivot_table.loc[keep_rows_mask, :].to_dict(orient="records")


@app.callback(Output("pie-chart", "children"), Input("budget-pivot-table-records", "data"))
def update_pie_chart(pivot_table_records: list[dict[str, float]]) -> dcc.Graph:
    pivot_table = pd.DataFrame(pivot_table_records)
    pie = go.Pie(labels=pivot_table["Category"], values=pivot_table["Amount"], hole=0.5)
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

    bar_chart = go.Bar(x=budget["Category"], y=budget["Amount"], name="Actual Expense")
    fig = go.Figure(data=[bar_chart])
    fig.update_layout(margin=dict(t=40, b=0, l=0, r=0), barmode="group")
    fig.update_traces(textposition="outside")
    return dcc.Graph(figure=fig)


if __name__ == "__main__":
    app.run_server(debug=True)
