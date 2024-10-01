import cloudscraper
from bs4 import BeautifulSoup
import urllib.parse
import time
import httpx
from .lib.objects import Search, SimpleTranslator
from .lib.settings import Settings


class Client:

	def __init__(self):
		self.scraper = cloudscraper.create_scraper()
		self.base_url = f"https://www.bing.com/search"
		self.settings.safeSearch(True)

	def search(self, query, type="search", pages=1):
		query = urllib.parse.quote_plus(query)
		results = []
		num_result_image = pages * 35
		num_result_search = pages * 10

		for page in range(pages):
			if type == "images":
				url = f"https://www.bing.com/images/async?q={query}&first={page * 35}&count=35"
				response = self.scraper.get(url)
				soup = BeautifulSoup(response.text, "html.parser")

				# Найти все изображения на странице
				for link in soup.find_all("a", {"class": "iusc"}):
					m = link.get("m")
					if m:
						m = eval(m.replace('null', 'None'))
						img_url = m.get("murl")
						if img_url and img_url.startswith("http"):
							results.append({"url": img_url, "description": ""})
							# Останавливаем поиск, если достигли нужного количества изображений
							if len(results) >= num_result_image:
								return Search(type, results)

			elif type == "search":
				headers = {
					"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
					"Cache-Control": "no-cache",
					"Pragma": "no-cache",
					"Accept-Language": "en-US,en;q=0.9",
					"Connection": "keep-alive",
				}
				url = f"{self.base_url}?q={query}&qs=HS&sc=4-0&cvid=65316F7498DF48CD8723778466B3B83A&FORM=QBLH&sp=1&lq=0&first={page*10}&count=10"
				response = self.scraper.get(url, headers=headers)
				
				soup = BeautifulSoup(response.text, "html.parser")

				if soup.find("li", {"class": "b_no"}):
					if soup.find('div', class_='b_vPanel'):
						return {"error": soup.find('div', class_='b_vPanel').div.get_text(strip=True)}
					return {"error": "No results found for this query."}

				for item in soup.find_all("li", {"class": "b_algo"}):
					link = item.find("a")
					description = item.find("p")
					if link:
						href = link.get("href")
						if href:
							text = link.get_text()
							desc = description.get_text() if description else ""
							results.append({"url": href, "description": desc})
							# Останавливаем поиск, если достигли нужного количества ссылок
							if len(results) >= num_result_search:
								return Search(type, results)

		return Search(type, results)

	def translate(self, text: str, to_language: str = "ru"):
		translated_text = SimpleTranslator().translate(text, target_language=to_language)
		return translated_text

	@property
	def settings(self):
		return Settings(self.scraper)