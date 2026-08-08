import asyncio
import aiohttp
from bs4 import BeautifulSoup
import pandas as pd
import time


async def fetch_page(session, url):
    async with session.get(url) as resp:
        soup = BeautifulSoup(await resp.text(), "lxml")

        qoutes = []
        for quote in soup.find_all("div", class_="quote"):
            quote_dct = {
                        "text": "", 
                        "author": "", 
                        "tags": ""
                    }

            text = quote.find("span", class_="text").text
            quote_dct["text"] = text

            author = quote.find("small", class_="author").text
            quote_dct["author"] = author

            tags = ", ".join([tag.text for tag in quote.find("div", class_="tags").find_all("a", class_="tag")])
            quote_dct["tags"] = tags

            qoutes.append(quote_dct)

        return qoutes    


async def main():
    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        all_quotes = []

        page = 1
        while True:
            url = f"https://quotes.toscrape.com/page/{page}"

            quotes = await fetch_page(session, url)

            if not quotes:
                break

            all_quotes.extend(quotes)

            page += 1

    if all_quotes:
        df = pd.DataFrame(all_quotes) 
        df.to_excel("parser_on_python_#3/quotes_async.xlsx", index=False)    
        print(f"{time.time() - start_time} seconds") 


if __name__ == "__main__":
    asyncio.run(main())


# синхронный такой же парсер

# import requests as req 
# from bs4 import BeautifulSoup 
# import pandas as pd
# import time

# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

# all_list = []

# start_time = time.time()

# for page in range(1, 11):
#     resp = req.get(f"https://quotes.toscrape.com/page/{page}/", headers=headers)

#     soup = BeautifulSoup(resp.text, "lxml")

#     data = soup.find_all("div", class_="quote")

#     for cit in data:
#         dct = {"Цитата": "", "Автор": "", "Теги": ""}

#         say = cit.find("span", class_="text").text
#         dct["Цитата"] = say
#         author = cit.find("small", class_="author").text
#         dct["Автор"] = author
#         tags = ", ".join([tag.text for tag in cit.find_all("a", class_="tag")])
#         dct["Теги"] = tags
        
#         all_list.append(dct)


# df = pd.DataFrame(all_list)
# df.to_excel("parser_on_python_#3/quots.xlsx", index=False)
# print(f"all right! {time.time() - start_time} seconds")