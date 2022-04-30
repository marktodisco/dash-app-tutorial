from typing import Callable, List, Protocol

from dash import Dash
from dash.dependencies import Input, Output


class Callback(Protocol):
    outputs: List[Output]
    inputs: List[Input]
    func: Callable  # I can't figure out a more descriptive type annotation


def register_callbacks(app: Dash) -> None:
    for callback in fetch_callbacks():
        app.callback(*callback.outputs, *callback.inputs)(callback.func)


def fetch_callbacks() -> List[Callback]:
    from src.callbacks.populate_tab_output import PopulateTabOutput
    from src.callbacks.update_category_dropdown import UpdateCategoryDropDown
    from src.callbacks.update_month_dropdown import UpdateMonthDropDown
    from src.callbacks.update_rolling_budget import UpdateRollingBudget
    from src.callbacks.update_year_dropdown import UpdateYearDropdown

    return [
        # UpdateCategoryDropDown(),
        # UpdateRollingBudget(),
        # UpdateMonthDropDown(),
        # UpdateYearDropdown(),
    ]
