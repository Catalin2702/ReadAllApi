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

path_mapping = {
	'novel': LnReader,
	'manga': MnReader,
	'manhwa': MnReader
}

urls = [
	'https://lnreader.org/search/autocomplete?{}',
	'https://readmanga.app/search/autocomplete?{}'
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
async def asyncRequestNovel():
	params = request.query_string.decode()
	params = parse_query_to_dict(params)
	coroutines = [fetch(url.format('&'.join([f"{key}={value}" for key, value in params.items()]))) for url in urls]
	results = await asyncio.gather(*coroutines)
	results = [result for results_from_url in results for result in results_from_url]
	return jsonify(results)


@app.route('/api/get_chapter', methods=['GET', 'POST'])
def requestNovelChapter():
	params = request.query_string.decode()
	params = parse_query_to_dict(params)
	print(params)
	reader = path_mapping[params.get('content_type')](params)
	return json.dumps(reader.get_chapters())


@app.route('/api/get_content/novel', methods=['GET', 'POST'])
@app.route('/api/get_content/manga', methods=['GET', 'POST'])
def requestNovelContent():
	raw_params = request.query_string.decode()
	params = parse_query_to_dict(raw_params)
	reader = path_mapping[params.get('content_type')](params)
	return json.dumps(reader.get_content())


if __name__ == '__main__':
	app.run()
