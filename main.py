import requests, os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from send_email import send_email

stock_list = ["ADVANC", "LH", "KTB", "MDX"]
stock_price_list = []

for stock in stock_list:
    url = f"https://www.set.or.th/th/market/product/stock/quote/{stock}/price"

    result = requests.get(url)
    src = result.content
    soup = BeautifulSoup(src, "html.parser")

    stock_price = soup.find("div", class_="stock-info").text
    stock_price = stock_price.strip()

    stock_price_list.append(stock_price)

load_dotenv()
recipient_email = os.getenv("RECIPIENT_EMAIL")
email_subject = "today stock price".title()
email_body = ""

stock_dict = dict(zip(stock_list, stock_price_list))
for stock, price in stock_dict.items():
    email_body += f"{stock}: {price}\n"

# print(email_body)

# Send email
send_email(recipient_email, email_subject, email_body)