import requests
from aiohttp import ClientSession
from bs4 import BeautifulSoup
import re
from urllib.parse import unquote

from template_extensions import TemplateReader


class MnReader(TemplateReader):

	async def _get_title(self):
		data = {
			'query': unquote(self.params.get('query')),
			'dataType': 'json'
		}
		url = self.url + '&'.join([f"{key}={value}" for key, value in data.items()])
		async with ClientSession() as session:
			async with session.get(url) as response:
				results = await response.json()
				if len(results) == 0:
					self.response = {}
				else:
					self.response = [{**result, 'type': self.content_type} for result in results.get('results')
									 if data['query'].lower() in result['original_title'].lower()]
			return self.response

	def _get_chapters(self):
		response = requests.get(self.url)
		if response.status_code == 200:
			soup = BeautifulSoup(response.text, 'html.parser')
			soup = soup.find_all(id=re.compile("^cmtb-"))
			soup = [so.find_all('a') for so in soup]
			soup_dict = {}
			for so in soup:
				for s in so:
					soup_dict[s.get_text().strip()] = s['href']
			self.response = soup_dict
		else:
			self.response = {}
		return self.response

	def _get_content(self):
		response = requests.get(self.url)
		if response.status_code == 200:
			soup = BeautifulSoup(response.text, 'html.parser')
			soup_div = soup.find('div', {'class': 'chapter-detail-novel-big-image'})
			soup_img = soup_div.find_all('img')
			soup_img = [img['src'] for img in soup_img]
			self.response = soup_img
		else:
			self.response = {}
		return self.response
