from dash import html, Dash
import pytest
import dash_bootstrap_components as dbc
from layout.components import app_layout
from layout.callbacks import register_callbacks
from selenium.webdriver.chrome.options import Options

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    ],
)
# Set the app layout
app.layout = app_layout()
# Register callbacks
register_callbacks(app)
# Set the page title
app.title = "AioSUT"


def pytest_setup_options():
    """pytest extra command line arguments for running
    faster"""
    options = Options()
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--headless")
    return options


def test_001_errorsinbuild(dash_duo):
    dash_duo.start_server(app, port=5000)
    dash_duo.wait_for_element("#project-info-button", timeout=5)
    assert (
        dash_duo.get_logs() == []
    ), "Browser console should contain no errors on build"
