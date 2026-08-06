import requests as req
from bs4 import BeautifulSoup
import pandas as pd 

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

resp = req.get("https://books.toscrape.com/catalogue/category/books/travel_2/index.html", headers=headers)

soup = BeautifulSoup(resp.text, "lxml")

data = soup.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

card_all = []

for i in data:
    in_card = "https://books.toscrape.com/catalogue/" + i.find("h3").find("a").get("href").replace("../", "")

    resp_in_card = req.get(in_card, headers=headers)

    soup_in_card = BeautifulSoup(resp_in_card.text, "lxml")

    card = {"Название": "", "Цена (£)": "", "Рейтинг": 0, "Наличие (шт)": 0, "Ссылка на картинку": ""}

    name = soup_in_card.find("div", class_="col-sm-6 product_main").find("h1").text
    card["Название"] = name

    price = soup_in_card.find("div", class_="col-sm-6 product_main").find("p", "price_color").text.replace("Â", "")
    card["Цена (£)"] = price

    raiting_tag = soup_in_card.find("div", class_="col-sm-6 product_main").find("p", "star-rating").get("class")

    raiting = 0

    if "One" in raiting_tag:
        raiting = 1
    elif "Two" in raiting_tag:
        raiting = 2
    elif "Three" in raiting_tag:
        raiting = 3
    elif "Four" in raiting_tag:
        raiting = 4
    else:
        raiting = 5 

    card["Рейтинг"] = raiting

    in_stock_str = soup_in_card.find("div", class_="col-sm-6 product_main").find("p", "instock availability").text.strip()
    in_stock = int("".join([char for char in in_stock_str if char.isdigit()]))
    card["Наличие (шт)"] = in_stock

    picture = "https://books.toscrape.com/" + soup_in_card.find("div", "col-sm-6").find("div", class_="item active").find("img").get("src").replace("../", "")
    card["Ссылка на картинку"] = picture

    card_all.append(card)

df = pd.DataFrame(card_all)
df.to_excel("travel_books.xlsx", index=False)

print("Well done! All correct!")