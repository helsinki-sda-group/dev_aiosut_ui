# %%
# Imports
from dash import Dash
import dash_bootstrap_components as dbc
from layout.components import app_layout
from layout.callbacks import register_callbacks

# Initialize the app
app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"},
    ],
)

# Set the server
server = app.server

# Set the app layout
app.layout = app_layout

# Register callbacks
register_callbacks(app)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
