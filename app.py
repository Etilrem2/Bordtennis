import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SPACELAB])
server = app.server

sidebar = html.Div(
    [
        html.Img(src="assets/ssb-logo.svg", style={"width": "230px"}),

        dbc.Nav(
            [

                dbc.NavLink(
                    [
                        html.Div(page["name"], className="ms-2"),
                    ],
                    href=page["path"],
                    active="exact",
                )
                for page in dash.page_registry.values()
            ],
            vertical=True,
            pills=True,

        )],
    style={"position": "fixed",
           "top": 0,
           "left": 0,
           "bottom": 0,
           "width": "16rem",
           'padding-top': '10px',
           "padding": "2rem 1rem",
           "background-color": "#075745",
           'font-family': 'sans-serif',
           'fontSize': '20px'},
)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div("Bordtenniskameratene",
                         style={'fontSize': 40, 'textAlign': 'center', "margin-left": "18rem", "margin-right": "2rem",
                                "padding": "2rem 1rem",
                                }))
    ]),

    html.Hr(),

    dbc.Row(
        [
            dbc.Col(
                [
                    sidebar
                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),

            dbc.Col(
                [
                    dash.page_container
                ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10)
        ]
    )
], fluid=True)

if __name__ == "__main__":
    app.run_server(debug=False, port='8081')
