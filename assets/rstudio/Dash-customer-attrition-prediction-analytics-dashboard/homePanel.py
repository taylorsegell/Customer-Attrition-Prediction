import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd



# Define the client button component


def client_button(id, name, risk, image):
    return html.P(
        html.Button(
            children=[
                html.Div(
                    className="row",
                    children=[
                        html.Div(
                            children=[
                                html.Img(src=image, width="100px",
                                         height="100px")
                            ],
                            className="col-3"
                        ),
                        html.Div(
                            children=[
                                html.H3(name),
                                html.H4(f"Attrition Risk: {risk}")
                            ],
                            className="col-9"
                        )
                    ]
                )
            ],
            style={"width": "100%"}
        ),
        id=f"client-btn-{id}"
    )


# Define the home panel layout
home_panel_layout = html.Div(
    [
        html.H2("Top Action Clients"),
        html.Br(),
        html.Div(
            [
                client_button(
                    id, clients[id]["name"], clients[id]["risk"], f"profiles/{clients[id]['image']}")
                for id in clientIds
            ]
        ),
        html.H2("Monthly Customer Attrition"),
        dcc.Graph(
            figure=go.Figure(
                data=[
                    go.Bar(
                        x=["January", "February", "March", "April",
                            "May", "June", "July", "August", "September"],
                        y=[4, 10, 9, 11, 13, 10, 8, 12, 9],
                        text=[4, 10, 9, 11, 13, 10, 8, 12, 9],
                        textposition="outside",
                        marker_color="steelblue"
                    )
                ],
                layout=go.Layout(
                    xaxis={"title": "Month"},
                    yaxis={"title": "Customers Attrited"},
                    barmode="stack"
                )
            ),
            style={"width": "600px", "height": "400px"}
        ),
        html.H2("Customers Attrition Risk"),
        dcc.Graph(
            figure=go.Figure(
                data=[
                    go.Pie(
                        labels=["Low Risk", "Medium Risk", "High Risk"],
                        values=[302, 135, 42],
                        textinfo="label+percent",
                        hole=0.3
                    )
                ],
                layout=go.Layout(legend={"title": "Risk Level"})
            ),
            style={"width": "600px", "height": "400px"}
        )
    ]
)

# Load the data and client information
clients = {
    "1": {"name": "Client 1", "risk": "Low", "image": "client1.png"},
    "2": {"name": "Client 2", "risk": "Medium", "image": "client2.png"},
    "3": {"name": "Client 3", "risk": "High", "image": "client3.png"}
}
clientIds = list(clients.keys())

# Set up the app layout
layout = html.Div(
    [
        html.H1("Dashboard"),
        home_panel
    ]
)

