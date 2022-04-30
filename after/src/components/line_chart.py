import locale
from functools import partial
from typing import List

import pandas as pd
from dash import dcc, html
from plotly import graph_objects as go
from src.data import load_transaction_data

locale.setlocale(locale.LC_ALL, "")
currency = partial(locale.currency, grouping=True)

__all__ = ["line_chart"]


class LineChart:
    _df: pd.DataFrame
    _pivot: pd.DataFrame
    _scatters: List[go.Scatter]  # type: ignore
    _fig: go.Figure  # type: ignore

    def create(self) -> go.Figure:  # type: ignore
        return self._fig

    def __init__(self) -> None:
        self._filter_transactions()
        self._create_pivot_table()
        self._create_scatters()
        self._create_figures()

    def _filter_transactions(self) -> None:
        cols = ["Index", "Date", "Account", "Description", "Label"]
        df = (
            load_transaction_data()
            .drop(columns=cols)
            .query("Category != ['Income', 'Ignore']")
            .query("Amount < 0")
        )
        df.loc[:, "Amount"] *= -1
        self._df = df

    def _create_pivot_table(self) -> None:
        pivot = self._df.pivot_table(index="Year", columns="Month", values="Amount", aggfunc="sum")
        pivot["Year"] = pivot.index
        pivot = (
            pivot.melt(id_vars="Year")
            .rename(columns={"value": "Amount"})
            .dropna()
            .sort_values(["Month"])
            .reset_index(drop=True)
        )
        self._pivot = pivot

    def _create_figures(self) -> None:
        fig = go.Figure(data=self._scatters)
        fig.update_layout(margin=dict(t=50, b=0, l=0, r=0), hovermode="x unified")
        fig.update_traces(mode="lines+markers")
        fig.update_xaxes(categoryorder="category ascending")  # type: ignore
        self._fig = fig

    def _create_scatters(self) -> None:
        scatters = []
        for year in sorted(self._pivot["Year"].unique(), reverse=True):
            df_filtered = self._pivot.query(f"Year == {year}").sort_values("Month")
            scatters.append(
                go.Scatter(
                    x=df_filtered["Month"],
                    y=df_filtered["Amount"].round(2),
                    name=f"{year}",
                    connectgaps=True,
                )
            )
        self._scatters = scatters


line_chart = html.Div(children=dcc.Graph(id="line-chart", figure=LineChart().create()))
