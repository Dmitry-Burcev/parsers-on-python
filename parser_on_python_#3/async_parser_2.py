import aiohttp
import asyncio
from bs4 import BeautifulSoup
import pandas as pd
import time

async def fetch_page(session, url):
    async with session.get(url) as resp:
        soup = BeautifulSoup(await resp.text(), "lxml")

        rows_on_one_page = []
        for row in soup.find("table").find_all("tr", class_="team"):
            Team_description = {
                "Name": "", 
                "Year": "", 
                "Wins": "", 
                "OT Losess": "", 
                "Win %": "", 
                "GF": "", 
                "GA": "", 
                "+/-": ""
            }

            name = row.find("td", class_="name").text.strip()
            Team_description["Name"] = name

            year = int(row.find("td", class_="year").text.strip())
            Team_description["Year"] = year

            wins = int(row.find("td", class_="wins").text.strip())
            Team_description["Wins"] = wins

            ot_losses = row.find("td", class_="ot-losses").text
            Team_description["OT Losess"] = ot_losses

            win_per = row.find("td", class_="pct text-success")
            if win_per is None or win_per == "":
                win_per = "None"
            else:
                win_per = float(win_per.text.strip())
            Team_description["Win %"] = win_per

            gf = int(row.find("td", class_="gf").text.strip())
            Team_description["GF"] = gf

            ga = int(row.find("td", class_="ga").text.strip())
            Team_description["GA"] = ga

            sucsess_text = row.find("td", class_="diff text-success")
            if sucsess_text is None or sucsess_text == "":
                sucsess_text = "None"
            else:
                sucsess_text = int(sucsess_text.text.strip())
            Team_description["+/-"] = sucsess_text

            rows_on_one_page.append(Team_description)

        return rows_on_one_page    


async def main():
    start_time = time.time()
    async with aiohttp.ClientSession() as session:
        urls = [f"https://www.scrapethissite.com/pages/forms/?page_num={i}" for i in range(1, 25)] 

        tasks = [fetch_page(session, url) for url in urls]
        all_page = await asyncio.gather(*tasks)

    result = []
    for page in all_page:
        result.extend(page)

    if result:  
        df = pd.DataFrame(result)
        df.to_excel("parser_on_python_#3/exel.xlsx", index=False)  
        print(time.time() - start_time)  


if __name__ == "__main__":
    asyncio.run(main())          

