import asyncio
from aiohttp import ClientSession
import json

from flask import Flask, request, jsonify
from novel_extensions import LnReader
from manga_extensions import MnReader
from _parser import parse_query_to_dict
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
CORS(app, resources={r"/*": {"origins": "*"}}, methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])


reader_mapping = [
	{
		'url': 'https://lnreader.org',
		'search_url': '/search/autocomplete?',
		'reader_url': 'https://lnreader.org',
		'content_type': 'novel',
		'obj': LnReader,
	},
	{
		'url': 'https://readmanga.app',
		'search_url': '/search/autocomplete?',
		'reader_url': 'https://rmanga.app/',
		'content_type': 'manhwa',
		'obj': MnReader
	}
]


async def fetch(url):
	async with ClientSession() as session:
		async with session.get(url) as response:
			results = await response.json()
			if 'lnreader' in url:
				content_type = 'novel'
			else:
				content_type = 'manhwa'
			return [{**result, 'type': content_type} for result in results.get('results')]


@app.route('/api/search', methods=['GET', 'POST'])
async def requestNovel():
	raw_params = request.query_string.decode()
	params = parse_query_to_dict(raw_params)
	readers = [reader['obj'](params, reader['url']+reader['search_url'], reader['content_type']) for reader in reader_mapping]
	coroutines = [reader.get_title() for reader in readers]
	results = await asyncio.gather(*coroutines)
	results = [result for results_from_url in results for result in results_from_url]
	return jsonify(results)


@app.route('/api/get_chapter', methods=['GET', 'POST'])
def requestNovelChapter():
	params = request.query_string.decode()
	params = parse_query_to_dict(params)
	reader = [reader['obj'](url=params.get('query'), content_type=params.get('content_type')) for reader in reader_mapping if reader['url'] in params.get('query')][0]
	return json.dumps(reader.get_chapters())


@app.route('/api/get_content/novel', methods=['GET', 'POST'])
@app.route('/api/get_content/manga', methods=['GET', 'POST'])
def requestNovelContent():
	raw_params = request.query_string.decode()
	params = parse_query_to_dict(raw_params)
	reader = [reader['obj'](url=params.get('query'), content_type=params.get('content_type')) for reader in reader_mapping if reader['reader_url'] in params.get('query')][0]
	return json.dumps(reader.get_content())


if __name__ == '__main__':
	app.run()
