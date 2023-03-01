def parse_query_to_dict(string_raw):
	list_of_string = string_raw.split('&')
	dict_to_return = {}
	dict_to_return.update(splitter(string) for string in list_of_string)
	return dict_to_return


def splitter(string):
	if '=' in string:
		sub_string = string.split('=')
		if ',' in sub_string[1] and sub_string[0] != 'query':
			return sub_string[0], sub_string[1].split(',')
		return sub_string[0], sub_string[1]
	else:
		return string, ''
