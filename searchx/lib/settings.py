import urllib.parse

class Settings:
	def __init__(self, scraper):
		self.scraper = scraper

	def safeSearch(self, status: bool = False):
		resp = self.scraper.get(f"https://www.bing.com/search?q={urllib.parse.quote_plus('sans')}")
		cookies = resp.cookies.get_dict()
		if status == False:
			self.scraper.cookies.update({"SRCHHPGUSR": "SRCHLANG=en&IG=456AC913196D477E83B1D67DD60625DA&BCML=0&BCSRLANG=&ADLT=OFF"})
		elif status == True:
			self.scraper.cookies.update({"SRCHHPGUSR": "SRCHLANG=en&IG=456AC913196D477E83B1D67DD60625DA&BCML=0&BCSRLANG=&ADLT=STRICT"})
		return {"saveSearchStatus": status}