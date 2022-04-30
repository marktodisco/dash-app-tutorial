from math import isclose

import dash_bootstrap_components as dbc
import pandas as pd
from dash import html
from src.app_utils import generate_random_id
from src.data import load_budget_data
from src.typing.aliases import BudgetRecordsAlias
from src.typing.classes import (
    BudgetDataFrame,
    BudgetTableDataFrame,
    BudgetTableDataFrameRow,
)

__all__ = ["create_budget_bars"]


def create_budget_bars(
    budget_pivot_table_records: BudgetRecordsAlias,
    rolling_enabled: bool,
    num_years: int,
    num_months: int,
) -> html.Div:
    planned_budget_df = compute_rolling_budget(
        load_budget_data(), rolling_enabled, num_years, num_months
    )
    expenses_df: BudgetDataFrame = pd.DataFrame(budget_pivot_table_records)  # type: ignore
    budget_table_df = compute_budget_table_df(planned_budget_df, expenses_df)
    budget_items = build_dash_budget_items(budget_table_df)
    return html.Div(children=budget_items)


def build_dash_budget_items(budget_table_df: BudgetTableDataFrame):
    budget_items: list[html.Div] = []
    row: BudgetTableDataFrameRow
    for _, row in budget_table_df.iterrows():  # type: ignore
        budget_items += [render_budget_item(row.Actual, row.Planned, row.Category)]
    return budget_items


def compute_budget_table_df(planned_budget_df: BudgetDataFrame, expenses_df: BudgetDataFrame):
    budget_table_df: BudgetTableDataFrame = pd.DataFrame(index=planned_budget_df.Category)  # type: ignore
    budget_table_df.reset_index(inplace=True)

    budget_table_df["Planned"] = planned_budget_df.Amount

    budget_table_df["Actual"] = -expenses_df.Amount  # Convert expenses to positive values
    budget_table_df["Actual"].fillna(0.0, inplace=True)  # type: ignore

    budget_table_df["Variance"] = budget_table_df.Planned - budget_table_df.Actual
    nan_mask = budget_table_df["Variance"].isna()
    budget_table_df.loc[nan_mask, "Variance"] = budget_table_df.loc[nan_mask, "Planned"]

    budget_table_df["Percentage"] = budget_table_df.Actual / budget_table_df.Actual.sum()
    return budget_table_df


def compute_rolling_budget(
    planned_budget: BudgetDataFrame, rolling_enabled: bool, num_years: int, num_months: int
) -> BudgetDataFrame:
    total_months = num_years * num_months if rolling_enabled else 1
    planned_budget.Amount = planned_budget.Amount * total_months
    return planned_budget


def render_budget_item(current_budget: float, max_budget: float, budget_title: str) -> html.Div:
    if current_budget >= max_budget:
        color = "danger"
    elif current_budget >= 0.75 * max_budget:
        color = "warning"
    else:
        color = "success"
    tooltip_target = f"budget-tooltip-target-{generate_random_id()}"
    if isclose(max_budget, 0.0):
        budget_used_percent = 0
    else:
        budget_used_percent = current_budget / max_budget * 100
    tooltip_text = f"Percent of Total: {budget_used_percent:.0f}%"
    return html.Div(
        className="pb-4",
        children=[
            html.Span(
                className="bugdet-item",
                children=[
                    html.Span(
                        id=tooltip_target,
                        children=[
                            html.Span(f"{budget_title}: ", className="budget-label"),
                            html.Span(f"${current_budget:.2f}", className="budget-text-value"),
                            html.Span("  of  ", className="budget-text"),
                            html.Span(f"${max_budget:.2f}", className="budget-text-value"),
                        ],
                    ),
                    dbc.Tooltip(
                        class_name="budget-tooltip",
                        children=[tooltip_text],
                        target=tooltip_target,
                    ),
                ],
            ),
            dbc.Progress(
                value=current_budget,
                min=0,
                max=max_budget,
                color=color,
                class_name="budget-progress-bar",
            ),
        ],
    )
