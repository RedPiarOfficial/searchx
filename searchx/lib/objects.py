import concurrent.futures
import os
try:
	from fake_useragent import UserAgent
except:
	os.system("pip install fake-useragent")
	from fake_useragent import UserAgent
import httpx

class Search:
	def __init__(self, type, data):
		self.type = type
		self.data = data

	def download(self, count , path="./img", threads=1):
		if self.type == "images":
			Threads(path, count, threads).download_images(self.data)
			return True
		else:
			return False

	def __repr__(self):
		return str(self.data)

	def __getitem__(self, key):
		if isinstance(self.data, dict):
			return self.data.get(key)
		elif isinstance(self.data, list):
			return self.data[key]
		else:
			raise Exception("Error")

class Threads:
	def __init__(self, path, count, threads):
		self.requests = httpx.Client(http2=True)
		self.ua = UserAgent()
		self.path = path
		self.threads = threads
		os.makedirs(self.path, exist_ok=True)
		self.count = count

	def download_image(self, idx, img_url):
		try:
			response = self.requests.get(img_url, headers={
				"User-Agent": self.ua.random
			}, timeout=2)
			if response.status_code in [200, 201]:
				with open(f"{self.path}/img_{idx}.png", "wb") as file:
					file.write(response.content)
		except Exception as e:
			pass

	# Загрузка изображений с многопоточностью
	def download_images(self, results):
		results = results[:self.count]
		with concurrent.futures.ThreadPoolExecutor(max_workers=self.threads) as executor:
			futures = []
			for idx, i in enumerate(results):
				futures.append(executor.submit(self.download_image, idx, i["url"]))

class SimpleTranslator:
	def __init__(self):
		self.base_url = "https://translate.googleapis.com/translate_a/single"
		self.requests = httpx.Client(http2=True)
	
	def translate(self, text: str, target_language: str = 'ru') -> str:
		"""
		Переводит текст с одного языка на другой, разбивая текст на части при необходимости.

		Args:
			text (str): Текст для перевода.
			target_language (str): Код языка для перевода (например, 'ru' для русского).

		Returns:
			str: Переведенный текст.
		"""
		# Функция для перевода одного фрагмента текста
		def translate_chunk(chunk: str) -> str:
			params = {
				'client': 'gtx',
				'sl': 'auto',
				'tl': target_language,
				'dt': 't',
				'q': chunk
			}
			response = self.requests.get(self.base_url, params=params)
			response.raise_for_status()
			result = response.json()
			# Извлечение переведенного текста
			return ''.join([item[0] for item in result[0]])

		# Разбиение текста на части
		chunk_size = 2000  # Максимально допустимый размер фрагмента, может потребоваться корректировка
		chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
		
		# Перевод каждой части и объединение результатов
		translated_chunks = [translate_chunk(chunk) for chunk in chunks]
		return ''.join(translated_chunks)