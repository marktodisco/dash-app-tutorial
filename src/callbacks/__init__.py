from typing import Callable

import dash


def register_callbacks(app: dash.Dash) -> None:
    for callback in collect_callbacks():
        callback(app)


def collect_callbacks() -> tuple[Callable[[dash.Dash], None], ...]:
    from . import (
        filter_budget_records,
        select_all_categories,
        select_all_months,
        select_all_years,
        update_pie_chart,
    )

    return (
        filter_budget_records.register,
        select_all_categories.register,
        select_all_months.register,
        select_all_years.register,
        update_pie_chart.register,
    )
