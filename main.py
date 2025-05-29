import requests
from bs4 import BeautifulSoup

stock_list = ["ADVANC", "LH", "KTB"]

for stock in stock_list:
    url = f"https://www.set.or.th/th/market/product/stock/quote/{stock}/price"

    result = requests.get(url)
    src = result.content
    soup = BeautifulSoup(src, "html.parser")

    stock_price = soup.find("div", class_="stock-info").text
    stock_price = stock_price.strip()

    print(f"{stock} - {stock_price}")