import argparse

from dash import Dash
import dash_bootstrap_components as dbc
from layout.components import app_layout
from layout.callbacks import register_callbacks


def create_app(visualization_mode="edge"):
    app = Dash(
        __name__,
        external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
        suppress_callback_exceptions=True,
        meta_tags=[
            {"name": "viewport", "content": "width=device-width, initial-scale=1"},
        ],
    )
    app.layout = app_layout()
    register_callbacks(app, visualization_mode=visualization_mode)
    app.title = "AIOSut"
    return app


def parse_args(args=None):
    parser = argparse.ArgumentParser(description="Run the AioSUT visualization app.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument(
        "--edge", action="store_const", const="edge", dest="mode",
        help="visualize air quality per road edge (default)",
    )
    mode.add_argument(
        "--cell", action="store_const", const="cell", dest="mode",
        help="visualize air quality using AQ grid cells",
    )
    parser.set_defaults(mode="edge")
    return parser.parse_args(args)


app = create_app()
server = app.server


if __name__ == "__main__":
    cli_args = parse_args()
    create_app(cli_args.mode).run(debug=True)
