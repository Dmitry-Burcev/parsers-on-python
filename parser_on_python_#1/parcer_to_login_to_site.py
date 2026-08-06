from requests import Session
from bs4 import BeautifulSoup 

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}

work = Session()

work.get("https://quotes.toscrape.com/", headers=headers)

resp = work.get("https://quotes.toscrape.com/login", headers=headers)

soup = BeautifulSoup(resp.text, "lxml")

token = soup.find("input").get("value")

data = {"csrf_token": token, "username": "bot_parcer", "password": "haha@bot"}

result = work.post("https://quotes.toscrape.com/login", headers=headers, data=data, allow_redirects=True)

if "Logout" in result.text:
    print("Correct! =)")
else: 
    print("Uncorrect =(")   