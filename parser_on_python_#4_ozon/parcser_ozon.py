import asyncio
import aiohttp
from bs4 import BeautifulSoup
import pandas as pd
import time


async def fetch_page(url, session):
    async with session.get(url) as resp:
        soup = BeautifulSoup(await resp.text(), "lxml")

        cards_on_page = []

        for card in soup.find("div", class_="search_d6a").find("div", id="contentScrollPaginator").find("div", class_="search_da5").find("div", class_="hj3_21").find_all("div", class_="tile-root g2p_21 h3j_21 h4j_21"):
            dct = {
                "type": "Laptop", 
                "brand": "asus", 
                "price": 0, 
                "now_status": "", 
                "description": ""
            }

            ob = card.find("div", class_="p2g_21")

            now_status = card.find("a").find("section").find("div", class_="q1b1_5_16-a3 b5_7_3-a0").find("div", class_="b5_7_3-a3").find("div", class_="b5_7_3-a4 tsBodyControl400Small").text.strip()
            dct["now_status"] = now_status

            price_with = ob.find("div", class_="qg1_21 qg2_21 c35_5_2-a c35_5_2-c0").find("div", class_="c35_5_2-a0").find("span", class_="c35_5_2-a1 tsHeadline500Medium c35_5_2-b2 c35_5_2-a6 c35_5_2-b0").text
            price = int("".join([num for num in price_with if num.isdigit()]))
            dct["price"] = price

            description = ob.find("div", class_="ea5_7_3-a").find("a").find("div", class_="bq03_9_1-a bq03_9_1-a4 bq03_9_1-a6 qg1_21").find("span", class_="tsBody500Medium").text.strip()
            dct["description"] = description

            cards_on_page.append(dct)

        return cards_on_page


async def main():
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        url = "https://www.ozon.ru/category/noutbuki-15692/asus-26303007/"

        tasks = [fetch_page(url=url, session=session)]
        start_tasks = await asyncio.gather(*tasks)

    result = []
    for card in start_tasks:
        result.extend(card)   

    if result:
        df = pd.DataFrame(result)
        df.to_excel("parser_on_python_#4_ozon/laptop_from_ozon.xlsx", index=False)
        print(f"Well done its {time.time() - start_time} seconds") 
    else:
        print("Whats wrong?")        


if __name__ == "__main__":
    asyncio.run(main())










