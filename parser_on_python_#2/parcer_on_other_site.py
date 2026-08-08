import requests as req 
from bs4 import BeautifulSoup 
import pandas as pd

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

all_list = []

for page in range(1, 11):
    resp = req.get(f"https://quotes.toscrape.com/page/{page}/", headers=headers)

    soup = BeautifulSoup(resp.text, "lxml")

    data = soup.find_all("div", class_="quote")

    for cit in data:
        dct = {"Цитата": "", "Автор": "", "Теги": ""}

        say = cit.find("span", class_="text").text
        dct["Цитата"] = say
        author = cit.find("small", class_="author").text
        dct["Автор"] = author
        tags = ", ".join([tag.text for tag in cit.find_all("a", class_="tag")])
        dct["Теги"] = tags
        
        all_list.append(dct)


df = pd.DataFrame(all_list)
df.to_excel("parser_on_python_#2/quots.xlsx", index=False)
print("all right!")

    