import smtplib
from datetime import date
import time
import schedule
import pandas as pd
from email.message import EmailMessage
import pandas as pd


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
       Denne månedens vinner er:


{str(vinner)}!
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






schedule.every().day.at("18:20").do(job)


while True:
    schedule.run_pending()
    time.sleep(30)

