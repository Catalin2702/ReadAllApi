class TemplateReader:

	params = None
	response = None
	url = None
	content_type = None

	def __init__(self, params=None, url=None, content_type=None):
		if params is None:
			params = {}
		self.params = params
		self.url = url
		self.content_type = content_type

	async def _get_title(self):
		raise NotImplementedError('Implement this method')

	async def get_title(self):
		return await self._get_title()

	def _get_chapters(self):
		raise NotImplementedError('Implement this method')

	def get_chapters(self):
		return self._get_chapters()

	def _get_content(self):
		raise NotImplementedError('Implement this method')

	def get_content(self):
		return self._get_content()
