import requests as req
from bs4 import BeautifulSoup
from time import sleep

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

for page in range(1, 51):
    sleep(3)
    url = f"https://books.toscrape.com/catalogue/page-{page}.html"

    resp = req.get(url, headers=headers)

    soup = BeautifulSoup(resp.text, "lxml")

    data = soup.find_all("li", class_="col-xs-6 col-sm-4 col-md-3 col-lg-3")

    for i in data:
        name = i.find("h3").text.strip()
        price = i.find("p", class_="price_color").text.strip().replace("Â", "")
        url_picture = "https://books.toscrape.com/" + i.find("img", class_="thumbnail").get("src").replace("../", "")

        print(f"{name}\n{price}\n{url_picture}\n\n")