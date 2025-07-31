import requests, os, csv
from datetime import datetime
from zoneinfo import ZoneInfo
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from send_email import send_email
from write_csv import write_csv
from read_json import json_to_list
from write_json import list_to_json

# Stock list to check
stock_json = "stocks.json"
stock_list = json_to_list(stock_json)

HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

BKK_TZ = ZoneInfo('Asia/Bangkok')


for index, stock in enumerate(stock_list):

    # Request URL
    url = f"https://www.set.or.th/th/market/product/stock/quote/{stock["symbol"]}/price"
    response = requests.get(url, headers=HEADERS)

    # File path
    file_path = os.path.join("data_csv", stock["symbol"] + ".csv")

    # For set.org when it can't find the url it will redirect to another page
    # So I check if there is a history.
    # If 0, it found the page
    if len(response.history) == 0:
        # Get html
        src = response.content
        soup = BeautifulSoup(src, "html.parser")

        # Get stock price
        stock_price = soup.find("div", class_="stock-info").text
        stock_price = stock_price.strip()

        # Get date and time
        date_time = datetime.now(BKK_TZ).strftime("%d %b %Y %H:%M:%S")

        # Data to write
        stock_data = {
            "date": date_time,
            "price": stock_price,
            "trend": "",
        }

        # Test
        # print("record data")
        # print(f"{stock["symbol"]}, {date_time}, {stock_price}")

        # If the price is greater than the max, update max to new max (+5%) and send an email
        if  float(stock_price) > stock["max"]:

            # Calculate new max, min
            stock["max"] = stock["max"] * 1.05
            stock["min"] = stock["min"] * 1.05
            stock_data["trend"] = "up"

            # Update min and max in stock_list
            stock_list[index]["max"] = stock["max"]
            stock_list[index]["min"] = stock["min"]

            # Write stock data to a csv file.
            write_csv(file_path,stock_data)

            # Write new min, max to stocks.json
            list_to_json(stock_list, stock_json)

            # Prepare for email
            load_dotenv()
            recipient_email = os.getenv("RECIPIENT_EMAIL")

            # Email message
            email_subject = "stock price alert!".title()
            email_body = f"On {date_time}, <b>{stock["symbol"]}</b> price is <b>{stock_price}</b>!<br><b>Trend:{stock_data["trend"]}</b> "

            # Send email
            send_email(recipient_email, email_subject, email_body, "html")

            # Test
            # print("sent email!")
            # print(email_body)

        # If the price is smaller than the min, update max to new max (-5%) and send an email
        elif float(stock_price) < stock["min"]:

            # Calculate new max, min
            stock["max"] = stock["max"] * 0.95
            stock["min"] = stock["min"] * 0.95
            stock_data["trend"] = "down"

            # Update min and max in stock_list
            stock_list[index]["max"] = stock["max"]
            stock_list[index]["min"] = stock["min"]

            # Write stock data to a csv file.
            write_csv(file_path,stock_data)

            # Write new min, max to stocks.json
            list_to_json(stock_list, stock_json)

            # Prepare for email
            load_dotenv()
            recipient_email = os.getenv("RECIPIENT_EMAIL")

            # Email message
            email_subject = "stock price alert!".title()
            email_body = f"On {date_time}, <b>{stock["symbol"]}</b> price is <b>{stock_price}</b>!<br><b>Trend:{stock_data["trend"]}</b> "

            # Send email
            send_email(recipient_email, email_subject, email_body, "html")

        else:

        # Write stock data to a csv file.
            write_csv(file_path,stock_data)

    else:

        # Cloud not get the page
        date_time = datetime.now(BKK_TZ).strftime("%d %b %Y %H:%M:%S")

        # Data to write
        stock_data = {
            "date": date_time,
            "price": "n/a",
            "trend": "n/a"
        }

        # Write stock data to a csv file.
        write_csv(file_path,stock_data)

        # Test
        # print(f"{date_time} Cloud not find the {stock["symbol"]} page!!!")
