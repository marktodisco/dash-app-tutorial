import argparse
import sys
from argparse import ArgumentParser
from dataclasses import dataclass

import dash_bootstrap_components as dbc
from dash import Dash

from layout import layout
from src.callbacks import register_callbacks


def main() -> None:
    args = parse_cli_args()
    run_app(args.debug)


@dataclass
class AppConfig:
    debug: bool


def parse_cli_args() -> AppConfig:
    parser = ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        "--debug",
        default=False,
        action="store_true",
        help="Run app in debug mode.",
    )
    args = parser.parse_args(sys.argv[1:])
    return AppConfig(debug=args.debug)


def run_app(debug: bool = False) -> None:
    app = create_app()
    register_callbacks(app)
    app.run_server(debug=debug)


def create_app() -> Dash:
    app = Dash(
        __name__,
        external_stylesheets=[dbc.themes.BOOTSTRAP, "https://codepen.io/chriddyp/pen/bWLwgP.css"],
    )
    app.title = "Financial Dashboard"
    app.layout = layout
    return app


if __name__ == "__main__":
    main()
