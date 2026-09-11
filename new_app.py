import argparse

from dash import Dash
import dash_bootstrap_components as dbc
from layout.components import app_layout
from layout.callbacks import register_callbacks


def create_app(
    visualization_mode="edge", show_liv=False, concentration_mode=False
):
    if concentration_mode and visualization_mode != "cell":
        raise ValueError("concentration_mode requires visualization_mode='cell'")
    app = Dash(
        __name__,
        external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
        suppress_callback_exceptions=True,
        meta_tags=[
            {"name": "viewport", "content": "width=device-width, initial-scale=1"},
        ],
    )
    app.layout = app_layout(show_liv=show_liv)
    register_callbacks(
        app,
        visualization_mode=visualization_mode,
        show_liv=show_liv,
        concentration_mode=concentration_mode,
    )
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
    parser.add_argument(
        "--concentration",
        action="store_true",
        help="visualize Enfuser concentrations using AQ grid cells",
    )
    parser.add_argument(
        "--show-liv",
        action="store_true",
        help="show the read-only livability priority derived from air quality",
    )
    parser.set_defaults(mode="edge")
    parsed = parser.parse_args(args)
    if parsed.concentration and parsed.mode != "cell":
        parser.error("--concentration requires --cell")
    return parsed


app = create_app()
server = app.server


if __name__ == "__main__":
    cli_args = parse_args()
    create_app(
        cli_args.mode,
        show_liv=cli_args.show_liv,
        concentration_mode=cli_args.concentration,
    ).run(debug=True)
