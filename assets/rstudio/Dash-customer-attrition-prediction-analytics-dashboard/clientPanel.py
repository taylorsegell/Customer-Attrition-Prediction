from lib.icp4d_api import cp4d_api_function
from lib.load_data import load_data
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State

# Import necessary libraries
import pandas as pd





# Load the data
data = load_data()

# Define the layout
client_layout = html.Div(
    [
        dcc.Tabs(
            [
                dcc.Tab(label="Client View", value="clientPanel", children=[
                    html.Br(),
                    html.Div(
                        className="pull-left",
                        children=[
                            html.Div(id="customerImage"),
                            html.H2(className="text-center",
                                    id="customerName"),
                        ],
                        style={"width": "25%"},
                    ),
                    html.Div(
                        children=[
                            html.H4("Personal Information",
                                    className="text-center"),
                            html.Hr(),
                            html.Div(id="customerInfo")
                        ]
                    ),
                    html.Div(
                        className="pull-right",
                        children=[
                            html.H4("Financial Profile",
                                    className="text-center"),
                            html.Hr(),
                            html.Div(id="customerFinancesInfo")
                        ],
                        style={"width": "25%", "float": "right"}
                    )
                ]),
                dcc.Tab(label="Account Details", value="accountDetails", children=[
                    html.H3("Account Details"),
                    html.Br(),
                    html.Table(id="customerAccountsTable"),
                    html.Br(),
                    html.Table(id="customerAccountSummaryTable")
                ]),
                dcc.Tab(label="Attrition Prediction", value="attritionPrediction", children=[
                    html.H3("Attrition Prediction"),
                    html.Br(),
                    html.Div(
                        [
                            html.Div(
                                id="authPanel",
                                children=[
                                    html.H4(
                                        "Connect to Cloud Pak for Data API"),
                                    dcc.Input(id="hostname",
                                              placeholder="CPD Hostname"),
                                    dcc.Input(id="username",
                                              placeholder="CPD Username"),
                                    dcc.Input(
                                        id="password", placeholder="CPD Password", type="password"),
                                    html.Button("Authenticate API", id="authBtn", n_clicks=0,
                                                className="btn-primary btn-lg btn-block", style={"max-width": "300px"}),
                                    html.Div(id="authError", style={
                                             "color": "red"})
                                ],
                                style={"max-width": "360px"}
                            ),
                            html.Div(
                                id="deploymentPanel",
                                children=[
                                    html.Div(
                                        children=[
                                            html.H4(
                                                "Model Scoring Pipeline Deployment"),
                                            dcc.Dropdown(
                                                id="deploymentSelector",
                                                options=[],
                                                value="",
                                                placeholder="Deployment:"
                                            ),
                                            html.P([
                                                html.Strong("Space Name: "),
                                                html.Span(
                                                    id="space_name", className="pull-right", style={"word-wrap": "break-word"})
                                            ]),
                                            html.P([
                                                html.Strong("GUID: "),
                                                html.Span(
                                                    id="deployment_guid", className="pull-right", style={"word-wrap": "break-word"})
                                            ]),
                                            html.P([
                                                html.Strong(
                                                    "Scoring Endpoint: "),
                                                html.Span(
                                                    id="scoring_url", className="pull-right", style={"word-wrap": "break-word"})
                                            ])
                                        ],
                                        style={"max-width": "360px"}
                                    ),
                                    html.Div(
                                        children=[
                                            html.Button(
                                                "Re-Authenticate", id="reauthenticateBtn", className="btn-primary btn-lg btn-block")
                                        ]
                                    )
                                ]
                            ),
                            html.Div(
                                id="scoreBtnSection",
                                children=[
                                    html.Div(
                                        className="pull-left",
                                        children=[
                                            html.Button("Predict Attrition", id="scoreBtn", n_clicks=0,
                                                        className="btn-primary btn-lg btn-block", style={"max-width": "300px"}),
                                            html.Br(),
                                            html.H4("Input JSON:"),
                                            html.Pre(id="pipelineInput"),
                                            html.Div(id="scoringError",
                                                     style={"color": "red"})
                                        ]
                                    ),
                                    html.Div(
                                        style={"width": "70%",
                                               "float": "right"},
                                        id="scoringResponse"
                                    )
                                ],
                                style={"display": "none"}
                            )
                        ]
                    )
                ])
            ],
            id="tabs",
            value="clientPanel"
        ),
    ]
)

# Define the callbacks


@app.callback(
    Output("customerName", "children"),
    Output("customerImage", "children"),
    Output("customerInfo", "children"),
    Output("customerFinancesInfo", "children"),
    Output("customerAccountsTable", "children"),
    Output("customerAccountSummaryTable", "children"),
    Output("pipelineInput", "children"),
    [Input("tabs", "value")],
    [State("tabs", "value")]
)
def update_client_view(selected_tab, current_tab):
    if selected_tab == "clientPanel":
        client = data["client"]

        customer_name = client["name"]
        customer_image = html.Img(
            src="profiles/" + client["image"],
            style={"display": "block", "margin-left": "auto",
                   "margin-right": "auto"},
            width=150,
            height=150
        )

        customer_info = html.Ul(
            className="list-unstyled",
            children=[
                html.Li([
                    html.Strong("Age: "),
                    html.Span(client["age_range"], className="pull-right",),
                    " years old"
                ]),
                html.Li([html.Strong("Marital Status: "), html.Span(
                    client["marital_status"], className="pull-right")]),
                html.Li([html.Strong("Address: "), html.Span(
                    client["address"], className="pull-right")]),
                html.Li([html.Strong("Profession: "), html.Span(
                    client["profession"], className="pull-right")]),
                html.Li([html.Strong("Level of Education: "), html.Span(
                    client["education_level"], className="pull-right")])
            ]
        )

        customer_finances_info = html.Ul(
            className="list-unstyled",
            children=[
                html.Li([html.Strong("Annual income: "), html.Span(
                    client["annual_income"], className="pull-right")]),
                html.Li([html.Strong("Home Owner: "), html.Span(
                    "Yes" if client["home_owner_indicator"] else "No", className="pull-right")]),
                html.Li([html.Strong("Monthly Housing: "), html.Span(
                    client["monthly_housing_cost"], className="pull-right")]),
                html.Li([html.Strong("Credit Score: "), html.Span(
                    round(client["credit_score"], 0), className="pull-right")]),
                html.Li([html.Strong("Credit Authority Level: "), html.Span(
                    client["credit_authority_level"], className="pull-right")])
            ]
        )

        customer_accounts_table = html.Table(
            className="table",
            children=[
                html.Thead(
                    html.Tr(
                        [html.Th(col) for col in ["Account ID", "Account Type", "Product ID", "Base Currency",
                                                  "Investment Objective", "Life Cycle Status", "Risk Tolerance", "Tax Advantage Indicator"]]
                    )
                ),
                html.Tbody(
                    [
                        html.Tr(
                            [html.Td(customer["account"][col]) for col in ["account_id", "account_type", "product_id", "base_currency",
                                                                           "investment_objective", "life_cycle_status", "risk_tolerance", "tax_advantage_indicator"]]
                        )
                    ]
                )
            ]
        )

        customer_account_summary_table = html.Table(
            className="table",
            children=[
                html.Thead(
                    html.Tr(
                        [html.Th(col) for col in ["Closing Balance", "Amount of Deposits", "Amount of Interest Earned",
                                                  "Number of Buy Trades", "Amount of Buy Trades", "Amount of Market Change"]]
                    )
                ),
                html.Tbody(
                    [
                        html.Tr(
                            [html.Td(customer["account_summary"][col]) for col in ["closing_balance", "amount_of_deposits",
                                                                                   "amount_of_interest_earned", "number_of_buy_trades", "amount_of_buy_trades", "amount_of_market_change"]]
                        )
                    ]
                )
            ]
        )

        pipeline_input = html.Pre(
            json.dumps(
                {"cust_id": client["id"], "sc_end_date": "2018-09-30"}, indent=2),
            id="pipelineInput"
        )

        return customer_name, customer_image, customer_info, customer_finances_info, customer_accounts_table, customer_account_summary_table, pipeline_input

    return "", "", "", "", "", "", ""


@app.callback(
    Output("space_name", "children"),
    Output("deployment_guid", "children"),
    Output("scoring_url", "children"),
    Output("scoreBtnSection", "style"),
    Output("authError", "children"),
    Output("authPanel", "style"),
    Output("deploymentSelector", "options"),
    Output("deploymentSelector", "value"),
    [Input("authBtn", "n_clicks")],
    [State("hostname", "value"), State("username", "value"), State(
        "password", "value"), State("deploymentSelector", "value")]
)
def authenticate_api(n_clicks, hostname, username, password, deployment_selector):
    if n_clicks == 0:
        return "", "", "", {"display": "none"}, "", "", [], ""

    # Authenticate API here
    try:
        deployments_resp = cp4d_api_function(
            hostname, username, password, "Customer-Attrition-Prediction-Scoring-Function-Deployment")
        deployments = deployments_resp["deployments"]
        token = deployments_resp["token"]
    except Exception as e:
        return "", "", "", {"display": "none"}, str(e), "", [], ""

    deployment_options = [{"label": deployment, "value": deployment}
                          for deployment in deployments]
    deployment_value = deployment_selector if deployment_selector in deployments else ""

    return deployments[deployment_value]["space_name"], deployments[deployment_value]["guid"], deployments[deployment_value]["scoring_url"], {}, "", {"max-width": "360px"}, deployment_options, deployment_value


@app.callback(
    Output("scoreBtnSection", "style"),
    [Input("reauthenticateBtn", "n_clicks")]
)
def reauthenticate_api(n_clicks):
    if n_clicks > 0:
        return {"display": "none"}

    return {}


@app.callback(
    Output("scoreBtnSection", "style"),
    [Input("deploymentSelector", "value"), Input("token", "value"),
     Input("allCustomers_rows_selected", "children")]
)
def enable_score_btn(deployment_selector, token, all_customers_rows_selected):
    if not deployment_selector or not token or not all_customers_rows_selected:
        return {"display": "none"}

    return {}


@app.callback(
    Output("scoringResponse", "children"),
    Output("scoringError", "children"),
    [Input("scoreBtn", "n_clicks"), Input("deploymentSelector", "value"), Input(
        "token", "value"), Input("allCustomers_rows_selected", "children")]
)
def score_model_deployment(n_clicks, deployment_selector, token, all_customers_rows_selected):
    if n_clicks == 0:
        return [], ""

    selected_deployment = deployments[deployment_selector]

    payload = {
        "fields": ["CUSTOMER_ID", "sc_end_date"],
        "values": [[all_customers_rows_selected, "2018-09-30"]]
    }

    try:
        response = scoreModelDeployment(
            selected_deployment["scoring_url"], payload, token)

        if "error" in response:
            return [], response["error"]
        elif "predictions" in response:
            result = response["predictions"][0]["values"]["predictions"][0]

            # Generate probability pie
            prob_values = result["values"][1]
            prob_df = pd.DataFrame(prob_values, columns=[
                                   "Probability"]).transpose()
            prob_df.columns = ["Prediction"]
            prob_df["Percentage"] = (
                prob_df["Probability"] * 100).round(1).astype(str) + "%"
            prob_df["Hover Text"] = prob_df["Prediction"] + \
                ": " + prob_df["Percentage"]

            prob_plot = get_prob_plot(prob_df)

            return [
                html.H3("Customer Attrition Prediction:"),
                html.P(prob_plot),
                html.Pre(json.dumps(result, indent=2), id="pipelineInput"),
            ], ""
    except Exception as e:
        return [], str(e)


if __name__ == "__main__":
    app.run_server(debug=True)
