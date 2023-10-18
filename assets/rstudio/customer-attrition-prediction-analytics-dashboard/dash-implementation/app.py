import dash
import dash_bootstrap_components as dbc

# Load required packages
import pandas as pd
import plotly.express as px

# Load datasets & CP4D API functions
from lib.load_data import load_data
from lib.icp4d_api import cp4d_api_function

# Import panels
from home_panel import home_panel_layout, home_panel_callbacks
from client_panel import client_panel_layout, client_panel_callbacks

# Create the app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Set the app title
app.title = "Customer Attrition Prediction"

# Load the data
data = load_data()

# Define the layout
app.layout = dbc.NavbarContainer(
    dbc.Navbar(
        [
            dbc.NavbarBrand("Customer Attrition Prediction", className="navbar-brand")
        ],
        color="dark",
        dark=True,
    ),
    id="navbar-container",
    fluid=True,
    className="navbar-container",
    children=[
        dbc.NavbarToggler(id="navbar-toggler"),
        dbc.Collapse(
            dbc.Tabs(
                [
                    dbc.Tab(label="Home", tab_id="home"),
                    dbc.Tab(label="Client", tab_id="client")
                ],
                id="tabs",
                active_tab="home",
                className="nav-tabs",
                card=True,
                fill=True
            ),
            id="navbar-collapse",
            navbar=True,
            is_open=True
        ),
        dbc.Container(
            [
                dbc.Row(
                    dbc.Col(id="tab-content-container", width=12),
                    justify="center"
                )
            ],
            fluid=True,
            className="content-container"
        )
    ]
)

# Define the callbacks
@app.callback(
    dash.dependencies.Output("tab-content-container", "children"),
    [dash.dependencies.Input("tabs", "active_tab")]
)
def render_tab_content(active_tab):
    if active_tab == "home":
        return home_panel_layout()
    elif active_tab == "client":
        return client_panel_layout(data)

home_panel_callbacks(app)
client_panel_callbacks(app)

if __name__ == "__main__":
    app.run_server(debug=True)
