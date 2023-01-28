import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import smtplib
from datetime import date
import time
import schedule
import pandas as pd
from email.message import EmailMessage

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SPACELAB])

def job():
    if date.today().day != 28:
        return

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

    vinner = df.Spiller.iloc[0]

    email_sender = 'erlendtilrem@gmail.com'
    email_password = 'mwdowhkjqumbhssw'
    email_reciever = 'etilrem@hotmail.com'

    subject = 'Vinneren er....'
    body = f"""
       Denne månedens vinner er: {str(vinner)}!
       """

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_reciever
    em['Subject'] = subject
    em.set_content(body)



    with open('Poeng/Elo.txt', 'w') as f:
        e = {'Eigil': 1000, 'Erlend': 1000, 'Jonas': 1000, 'Kjetil': 1000}

        for key, value in e.items():
            f.write(key + ' ' + str(value) + '\n')
    f.close()



    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_reciever, em.as_string())







sidebar = html.Div(
    [
        html.Img(src="assets/ssb-logo.svg", style={"width": "230px", 'padding-bottom' : '20px'}),

        dbc.Nav(
            [

                dbc.NavLink(
                    [
                        html.Div(page["name"], className="ms-2"),
                    ],
                    href=page["path"],
                    active="exact",
                    style = {'color': 'black'}
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
           'fontSize': '20px',
           },
)

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.Div("Bordtenniskameratene",
                         style={'fontSize': 40, 'textAlign': 'center', "margin-left": "18rem", "margin-right": "2rem",
                                "padding": "2rem 1rem", "color": "black"
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
    app.run_server(debug=False)

schedule.every().day.at("17:30").do(job)

while True:
    schedule.run_pending()
    time.sleep(1)