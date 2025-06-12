import requests, os
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from send_email import send_email

# Stock list
stock_list = [
    {
    "symbol": "MDX",
    "min": 2.5,
    "max": 3.0,
    },
    {
    "symbol": "GULF",
    "min": 41.0,
    "max": 46.0,
    }
    ]

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

BKK_TZ = ZoneInfo('Asia/Bangkok')

for stock in stock_list:
    url = f"https://www.set.or.th/th/market/product/stock/quote/{stock["symbol"]}/price"
    response = requests.get(url, headers=HEADERS)

    # For set.org when it can't find the url it will redirect to another page
    # So I check if there is a history, it cloud not find the page
    if len(response.history) == 0:
        # Get html
        src = response.content
        soup = BeautifulSoup(src, "html.parser")

        # Get stock price
        stock_price = soup.find("div", class_="stock-info").text
        stock_price = stock_price.strip()

        # Email message
        load_dotenv()
        recipient_email = os.getenv("RECIPIENT_EMAIL")

        # Get date and time
        date_time = datetime.now(BKK_TZ).strftime("%d %b %Y %H:%M:%S")

        email_subject = "stock price alert!".title()
        email_body = f"On {date_time}, <b>{stock["symbol"]}</b> price is <b>{stock_price}</b>!"


        # If the price is outside the threshold, send an email
        if float(stock_price) < stock["min"] or float(stock_price) > stock["max"]:
            # Send email
            # send_email(recipient_email, email_subject, email_body, "html")
            print("sent email!")
            print(email_body)
        else:
            # Test print email body
            print("record data")
            print(f"{stock["symbol"]}, {date_time}, {stock_price}")

    else:
        date_time = datetime.now(BKK_TZ).strftime("%d %b %Y %H:%M:%S")
        print(f"{date_time} Cloud not find the {stock["symbol"]} page!!!")
