import dash
from dash import dcc, html, callback, Output, Input, dash_table
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from funksjoner.elo import expected, elo
import datetime
import dash_core_components as dcc

dash.register_page(__name__, name='Spillerrating')

kolonner = ['Spiller', 'Rating']

layout = html.Div(
    [

        dash_table.DataTable(
            id='tabell_rating',
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

        html.Button('Hent rating', id='save', n_clicks=0,
                    style={"background-color": "#C78800", "margin-left": "50%", 'height': '37px',
                           'horizontalAlign': 'middle'}),

        html.Div(id='countdown-container', children=[
            html.H1(id='countdown-text', style={'width': '100%', 'textAlign': 'center'}),
            dcc.Interval(id='interval-component', interval=1 * 1000, n_intervals=0)])

        # html.H1(id='countdown-text', style = {'margin-left' : '50%', 'horizontalAlign' : 'middle'}),
        # dcc.Interval(id='interval-component', interval=1*1000, n_intervals=0)
    ]
)


@callback(
    Output('tabell_rating', 'data'),
    Input('save', 'n_clicks')
)
def update_tabell(lagre):
    if lagre > 0:

        e = {}

        with open("Poeng/Elo.txt", 'r') as f:
            for linje in f:
                (spiller, rating) = linje.split()
                e[spiller] = rating

        f.close()

        df = pd.DataFrame.from_dict(e, orient='index').reset_index()
        df.columns = 'Spiller', 'Rating'

        kolonner = df.columns.tolist()

        df['Rating'] = df['Rating'].astype('int')
        df.sort_values(by='Rating', inplace=True, ascending=False)

    return df.to_dict('records')


@callback(
    Output(component_id='countdown-text', component_property='children'),
    [Input(component_id='interval-component', component_property='n_intervals')]
)
def update_countdown(n):
    today = datetime.datetime.now()
    if today.month == 12:
        next_month = 1
        next_year = today.year + 1
    else:
        next_month = today.month + 1
        next_year = today.year

    end_of_month = datetime.datetime(next_year, next_month, 1) - datetime.timedelta(days=1)
    time_until_end = end_of_month - today
    time_until_end_seconds = int(time_until_end.total_seconds())

    if time_until_end_seconds < 60:
        with open('Poeng/Elo.txt', 'w') as f:
            e = {'Eigil': 1000, 'Erlend': 1000, 'Jonas': 1000, 'Kjetil': 1000}

            for key, value in e.items():
                f.write(key + ' ' + str(value) + '\n')

    return 'Tid til reset: {} dager, {} timer, {} minutt, {} sekund'.format(time_until_end.days,
                                                                            time_until_end.seconds // 3600,
                                                                            (time_until_end.seconds // 60) % 60,
                                                                            (time_until_end.seconds) % 60)

