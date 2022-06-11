import dash_bootstrap_components as dbc
from dash import Dash

import src


def main() -> None:
    app = Dash(
        __name__,
        external_stylesheets=[dbc.themes.BOOTSTRAP, "https://codepen.io/chriddyp/pen/bWLwgP.css"],
    )
    app.title = "Financial Dashboard"
    app.layout = src.layout.create_layout()
    src.callbacks.register_callbacks(app)
    app.run_server(debug=True)


if __name__ == "__main__":
    main()
