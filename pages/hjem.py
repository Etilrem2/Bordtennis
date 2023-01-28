import dash
from dash import dcc, html, callback, Output, Input, dash_table
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

dash.register_page(__name__, path='/', name='Hjem')  # '/' is home page

kolonner = ['Spiller', 'Kamper spilt', 'Vunnet', 'Tapt']

layout = html.Div(
    [
        dbc.Row(
            [

                dbc.Col(
                    [

                        dash_table.DataTable(
                            id='tabell',
                            columns=[{"name": i, "id": i} for i in kolonner],
                            style_cell={'fontSize': 25, 'font-family': 'sans-serif'},
                            page_size=20,
                            fixed_rows={'headers': True},
                            style_table={'height': 200, 'overflowY': 'auto', 'padding-top': '20px', 'width': '50%',
                                         'margin-left': 'auto', 'margin-right': 'auto'},
                            style_data={
                                'whiteSpace': 'normal',
                                'height': 'auto',
                                'textOverflow': 'ellipsis',
                                'maxWidth': 0
                            }),

                        html.Button('Oppdater tabell', id='save', n_clicks=0,
                                    style={"background-color": "#C78800", "margin-left": "50%", 'height': '37px',
                                           'horizontalAlign': 'middle'})

                    ], xs=12, sm=12, md=3, lg=3, xl=6, xxl=6,
                )

            ]
        )

    ]
)


@callback(
    Output('tabell', 'data'),
    Input('save', 'n_clicks')
)
def update_tabell(lagre):
    if lagre > 0:
        d = {}

        with open("Poeng/Poeng.txt", 'r') as f:
            for linje in f:
                (spiller, spilt, seier, tap) = linje.split()
                d[spiller] = spilt, seier, tap
        f.close()

        df = pd.DataFrame.from_dict(d, orient='index').reset_index()
        df.columns = 'Spiller', 'Kamper spilt', 'Vunnet', 'Tapt'

        kolonner = df.columns.tolist()

        df['Vunnet'] = df['Vunnet'].astype('int')
        df.sort_values(by='Vunnet', inplace=True, ascending=False)

    return df.to_dict('records')
