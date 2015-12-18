#!/usr/bin/python

import readline, requests
from bs4 import BeautifulSoup

def indent(text):
	return '\n'.join('  ' + x for x in text.split('\n'))

url = 'http://api.wolframalpha.com/v2/query'
appid = 'Your API key here'  # get one at https://developer.wolframalpha.com/portal/apisignup.html

while True:
	try:
		query = raw_input('W|A> ')
	except EOFError:
		print
		break
	except KeyboardInterrupt:
		print
		continue
	if query.strip() == '':
		continue
	xml = requests.get(url, params=dict(input=query, appid=appid, format='plaintext')).text

	bs = BeautifulSoup(xml, 'xml')
	if bs.queryresult['success'] == 'true':
		for pod in bs.find_all('pod'):
			if len(pod.plaintext.contents):
				print '\033[1m\033[92m%s\033[0m' % pod['title']
				print indent('\n'.join(pod.plaintext.contents))
	else:
		print '\033[91mQuery failed'
		for tip in bs.find_all('tip'):
			print '\033[93m-', tip['text']
		print '\033[0m',
