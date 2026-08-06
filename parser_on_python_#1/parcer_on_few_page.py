import requests as req
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

all_books = []

def get_url():
    for page in range(1, 5):
        url = f"https://books.toscrape.com/catalogue/page-{page}.html"

        resp = req.get(url, headers=headers)

        soup = BeautifulSoup(resp.text, "lxml")

        data = soup.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

        for i in data:
            card_url = "https://books.toscrape.com/catalogue/" + i.find("a").get("href")
            yield card_url


for card in get_url():
    sleep(0.1)
    resp = req.get(card, headers=headers)
    
    soup = BeautifulSoup(resp.text, "lxml")

    data = soup.find("div", class_="col-sm-6 product_main")

    name = data.find("h1").text

    book_info = {"Название": name}

    rows = soup.find_all("tr")

    for row in rows:
        th = row.find("th").text
        td = row.find("td").text

        if "Â" in td:
            td = td.replace("Â", "")
        book_info[th] = td

    all_books.append(book_info)

df = pd.DataFrame(all_books)
df.to_excel("books.xlsx", index=False)

print(f"All right! {len(all_books)} added to table.")

       
        
        
        