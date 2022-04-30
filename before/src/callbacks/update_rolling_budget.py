from dash import dcc
from dash.dependencies import Input, Output


class UpdateRollingBudget:
    outputs = [Output("rolling-budget-div", "children")]
    inputs = [
        Input("year-dropdown", "value"),
        Input("month-dropdown", "value"),
        Input("tabs-group", "value"),
    ]

    def func(self, years: list[int], months: list[str], selected_tab: str) -> dcc.Checklist:
        if (selected_tab == "tab-3") and (len(years) != 1 or len(months) != 1):
            disabled = False
        else:
            disabled = True
        return dcc.Checklist(
            options=[{"label": "Rolling Budget", "value": "Rolling Budget", "disabled": disabled}],
            value=["Rolling Budget"] if not disabled else [],
            id="my-checklist",
        )
