from datetime import datetime
import pytz
from finvizfinance.screener.overview import Overview
import pandas as pd
import requests
import yfinance as yf
import time as t

time = pytz.timezone('America/New_York')
old_stocks_list=[]
new_stocks_list=[]

def get_stocks_list():
    a = Overview()
    filters_dict = {'Relative Volume': 'Over 3', 'Performance': 'Today Up', 'Float': 'Under 20M', 'Price': 'Under $20'}
    a.set_filter(filters_dict=filters_dict, signal="Unusual Volume")
    df = a.screener_view()
    return df['Ticker'].tolist()

def send_telegram_msg(message):
    chat_id = "-4117008991"
    TOKEN = "6773097784:AAFyxMBuiHsJ-V9HBa86DWq5pBAx3hRcCjE"
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url).json()

def generate_msg(lst):
    str=""
    for stock in lst:
        str=f"{str}{stock} : {yf.Ticker(stock).info['currentPrice']}\n"

    return str

def telegram_check():
    import requests
    TOKEN = "6773097784:AAFyxMBuiHsJ-V9HBa86DWq5pBAx3hRcCjE"
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    print(requests.get(url).json())

old_stocks_list = ['CETY', 'CCG', 'CNVS', 'CHNR', 'RAYA', 'BREA', 'HOUR', 'ATXG', 'IINN', 'HCTI', 'TAOP', 'TIRX', 'ARYD', 'TGL', 'ENGN', 'GLSI', 'MFV', 'BOTJ', 'WTO', 'ELMD', 'TNON', 'MGOL', 'PWUP', 'BAOS', 'BWAQ', 'LEJU', 'AFAR', 'BYU', 'PTPI', 'ELVN', 'CRWS', 'OSS', 'ESAC', 'MTEK', 'PBLA', 'ATIP', 'SSTI', 'LFLY', 'FLUX', 'BMR', 'TC', 'JAN', 'STI']

while(True):
    now = datetime.now(time)
    if(now.hour==16 and (now.minute==30 or now.minute==31)):
        old_stocks_list = get_stocks_list()
        t.sleep(120)

    elif(now.hour==10 and (now.minute==0 or now.minute==1)):
        new_stocks_list = get_stocks_list()
        diff = list(set(new_stocks_list) - set(old_stocks_list))
        send_telegram_msg(generate_msg(diff))
        t.sleep(120)

    t.sleep(60)



