import requests
from bs4 import BeautifulSoup
import re
from urllib.parse import unquote


class MnReader:

	params = {}
	response = {}
	url = 'https://readmanga.app/search/autocomplete?'

	def __init__(self, params: dict):
		self.params = params

	def __get_title(self):
		data = {
			'query': unquote(self.params.get('query')),
			'dataType': 'json'
		}
		response = requests.get(url=self.url, params=data)
		if response.status_code == 200 and len(response.json()) > 0:
			self.response = response.json().get('results')
			for res in self.response:
				res['type'] = 'Manhwa'

	def get_title(self):
		self.__get_title()
		return self.response

	def __get_chapters(self):
		response = requests.get(url=self.params.get('query'))
		if response.status_code == 200:
			soup = BeautifulSoup(response.text, 'html.parser')
			soup = soup.find_all(id=re.compile("^cmtb-"))
			soup = [so.find_all('a') for so in soup]
			soup_dict = {}
			for so in soup:
				for s in so:
					soup_dict[s.get_text().strip()] = s['href']
			self.response = soup_dict

	def get_chapters(self):
		self.__get_chapters()
		return self.response

	def __get_content(self):
		response = requests.get(url=self.params.get('query'))
		if response.status_code == 200:
			soup = BeautifulSoup(response.text, 'html.parser')
			soup_div = soup.find('div', {'class': 'chapter-detail-novel-big-image'})
			soup_img = soup_div.find_all('img')
			soup_img = [img['src'] for img in soup_img]
			self.response = soup_img

	def get_content(self):
		self.__get_content()
		return self.response
