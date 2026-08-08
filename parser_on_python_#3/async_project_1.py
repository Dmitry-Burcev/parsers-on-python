import asyncio
import aiohttp
from bs4 import BeautifulSoup
import pandas as pd
import time


async def fetch_page(session, url):
    async with session.get(url) as resp:
        soup = BeautifulSoup(await resp.text(), "lxml")

        pages_on_one_page = []

        for page in soup.find_all("div", class_="product-card css-e8at8d eag3qlw10"):
            page_dct = {
                "name": "", 
                "price": "", 
                "raiting": 0, 
                "picture-url": ""
            }

            name = page.find("a", class_="card-header css-o171kl eag3qlw2").find("h4", class_="title css-7u5e79 eag3qlw7").text
            page_dct["name"] = name

            price = page.find("div", class_="price-wrapper css-li4v8k eag3qlw4").text
            page_dct["price"] = price

            raiting = len(page.find("div", class_="rating css-1lp4z4h e15c0rei0").find_all("svg", class_="css-1cftdwf eag3qlw6"))
            page_dct["raiting"] = raiting

            picture_url = "https://sandbox.oxylabs.io" + page.find("span").find("img").get("src").replace("../", "")
            page_dct["picture-url"] = picture_url

            pages_on_one_page.append(page_dct)

        return pages_on_one_page


async def main():
    start_time = time.time()

    async with aiohttp.ClientSession() as session:
        urls = [f"https://sandbox.oxylabs.io/products?page={i}" for i in range(1, 95)]

        tasks = [fetch_page(session, url) for url in urls]

        all_pages = await asyncio.gather(*tasks)

    all_pages_list = []
    for page in all_pages:
        all_pages_list.extend(page)

    if all_pages_list:
        df = pd.DataFrame(all_pages_list)
        df.to_excel("parser_on_python_#3/oxylabs_products.xlsx", index=False)
        print(time.time() - start_time)  


if __name__ == "__main__":
    asyncio.run(main())              


            