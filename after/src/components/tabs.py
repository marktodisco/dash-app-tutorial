from typing import Any, Dict, List

import pandas as pd
from dash import dcc, html
from plotly import graph_objects as go

__all__ = [
    "tabs",
    "update_bar_chart",
    "update_pie_chart",
]


tabs = html.Div(
    className="mt-4 tabs-group",
    children=[
        dcc.Tabs(
            id="tabs-group",
            value="tab-3",
            children=[
                dcc.Tab(label="Budget Table", value="tab-3"),
                dcc.Tab(label="Pie Chart", value="tab-1"),
                dcc.Tab(label="Bar Chart", value="tab-2"),
            ],
        ),
        html.Div(
            className="checklist",
            children=[dcc.Checklist(id="my-checklist")],
            id="rolling-budget-div",
        ),
        html.Div(id="tab-output"),
    ],
)


def update_pie_chart(
    budget_records: List[Dict[str, Any]],
) -> go.Figure:  # type: ignore
    budget = budget_records_to_df(budget_records)
    pie = go.Pie(labels=budget["Category"], values=budget["Amount"], hole=0.5)
    fig = go.Figure(data=[pie])
    fig.update_layout(margin=dict(t=40, b=0, l=0, r=0))
    fig.update_traces(hovertemplate="%{label}<br>$%{value:.2f}<extra></extra>")
    return fig


def update_bar_chart(
    budget_records: List[Dict[str, Any]], planned_budget: pd.DataFrame
) -> go.Figure:  # type: ignore
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
    return fig


def budget_records_to_df(budget_records: List[Dict[str, Any]]) -> pd.DataFrame:
    budget = pd.DataFrame(budget_records)
    for idx, row in budget.iterrows():
        if row["Amount"] > 0:
            budget = budget.loc[budget.index != idx, :]
    budget["Amount"] = -budget["Amount"]
    budget = budget.query("Amount > 0")
    return budget
