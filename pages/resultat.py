import dash
from dash import dcc, html, callback, Output, Input, State, dash_table
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from funksjoner.elo import expected, elo

dash.register_page(__name__, name='Registrer resultat')

d = {}

with open("Poeng/Poeng.txt", 'r') as f:
    for linje in f:
        (spiller, spilt, seier, tap) = linje.split()
        d[spiller] = spilt, seier, tap
f.close()

df = pd.DataFrame.from_dict(d, orient='index').reset_index()
df.columns = 'Spiller', 'Kamper spilt', 'Vunnet', 'Tapt'

kolonner = df.columns.tolist()

layout = html.Div(
    [
        html.Div(
            [
                dcc.Input(
                    id='passord',
                    type='password',
                    placeholder='Passord:',
                    disabled=False,
                    readOnly=False,
                    style={'color' : 'black'},

                )

            ]),

        dcc.Markdown("Vinner:",
                     style={'width': '35%', 'display': 'inline-block', 'fontSize': 25, 'textAlign': 'right', 'color' : 'black'}),
        dcc.Dropdown(options=df.Spiller.unique(), id='vinner',
                     style={'width': '50%', 'height': '30px', 'display': 'inline-block', 'textAlign': 'left',
                            'padding-left': '20px', 'padding-bottom' : '10px'}),

        html.Div(
            [

                dcc.Markdown("Taper:",
                             style={'width': '35%', 'display': 'inline-block', 'fontSize': 25, 'textAlign': 'right', 'color' : 'black'}),
                dcc.Dropdown(options=df.Spiller.unique(), id='taper',
                             style={'width': '50%', 'height': '30px', 'display': 'inline-block', 'textAlign': 'left',
                                    'padding-left': '20px'}),

                dbc.Button('Registrer resultat', id='save', n_clicks=0, className = 'mt-2 mb-4 border',
                            style={"background-color": "#C78800", "margin-left": "40%", 'height': '37px',
                                   'horizontalAlign': 'middle'}),



                html.Div(id='my-output', style={"margin-left": "300px"}),

            ])

    ])


@callback(
    Output('my-output', 'children'),
    Output('passord', 'value'),
    State('passord', 'value'),
    State('vinner', 'value'),
    State('taper', 'value'),
    Input('save', 'n_clicks')

)
def resultat(passord, vinner, taper, lagre, ):
    if passord != 'Erlenderkul123' and lagre > 0:
        return 'Godt forsøk, Eigil...', ''

    if vinner == taper and lagre > 0:
        return 'Det går ikke...', ''

    if passord == 'Erlenderkul123' and lagre > 0 and vinner != taper:
        d = {}

        with open("Poeng/Poeng.txt", 'r') as f:
            for linje in f:
                (spiller, spilt, seier, tap) = linje.split()
                d[spiller] = spilt, seier, tap
                if spiller == vinner:
                    d[spiller] = int(spilt) + 1, int(seier) + 1, tap
                if spiller == taper:
                    d[spiller] = int(spilt) + 1, seier, int(tap) + 1
        f.close()

        with open('Poeng/Poeng.txt', 'w') as f:
            for key, value in d.items():
                f.write(key + ' ' + str(value[0]) + ' ' + str(value[1]) + ' ' + str(value[2]) + '\n')
        f.close()

        e = {}

        with open("Poeng/Elo.txt", 'r') as f:

            for linje in f:
                (spiller, rating) = linje.split()
                e[spiller] = rating

            forventa_poengsum_vinner = expected(int(e[vinner]), int(e[taper]))
            e[vinner] = round(elo(int(e[vinner]), forventa_poengsum_vinner, 1))

            forventa_poengsum_taper = expected(int(e[taper]), int(e[vinner]))
            e[taper] = round(elo(int(e[taper]), forventa_poengsum_taper, 0))

        f.close()

        with open('Poeng/Elo.txt', 'w') as f:
            for key, value in e.items():
                f.write(key + ' ' + str(value) + '\n')
        f.close()

        return 'Resultat lagret!', ''


