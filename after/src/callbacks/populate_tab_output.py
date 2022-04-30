from typing import Any, Dict, List, Union

from dash import dcc, html
from dash.dependencies import Input, Output
from src.components.budget_bars import create_budget_bars
from src.components.tabs import update_bar_chart, update_pie_chart
from src.data import load_budget_data

planned_budget = load_budget_data()


class PopulateTabOutput:
    rolling_enabled: bool = False

    outputs = [Output("tab-output", "children")]
    inputs = [
        Input("tabs-group", "value"),
        Input("budget-pivot-table-records", "data"),
        Input("my-checklist", "value"),
        Input("year-dropdown", "value"),
        Input("month-dropdown", "value"),
    ]

    def func(
        self,
        selected_tab: str,
        budget_records: List[Dict[str, Any]],
        checklist_values: List[str],
        years: List[int],
        months: List[str],
    ) -> html.Div:
        if len(budget_records) == 0:
            return self.handle_empty_records()

        self.check_if_rolling_budget_enabled(checklist_values)

        if selected_tab == "tab-1":
            return html.Div(children=dcc.Graph(figure=update_pie_chart(budget_records)))
        elif selected_tab == "tab-2":
            return html.Div(
                children=dcc.Graph(figure=update_bar_chart(budget_records, planned_budget))
            )
        else:
            return html.Div(
                id="budget-bars-div",
                children=html.Div(
                    create_budget_bars(
                        budget_records,
                        self.rolling_enabled,
                        len(years),
                        len(months),
                    )
                ),
            )

    def check_if_rolling_budget_enabled(self, checklist_values: List[str]) -> None:
        if self.is_valid_rolling_budget(checklist_values):
            self.rolling_enabled = True
        else:
            self.rolling_enabled = False

    @staticmethod
    def is_valid_rolling_budget(checklist_values: Union[List[str], str]) -> bool:
        return (
            isinstance(checklist_values, list)
            and len(checklist_values) == 1
            and checklist_values[0] == "Rolling Budget"
        )

    @staticmethod
    def handle_empty_records() -> html.Div:
        return html.Div(children=["No data selected."], style={"text-align": "center"})
