#!/usr/bin/python

import argparse, codecs, os, readline, requests, urllib
from bs4 import BeautifulSoup
from mako.template import Template

try:
	readline.read_history_file(os.path.expanduser('~/.wash.history'))
except IOError:
	pass

buffer = []

def write_html(fp):
	template = Template('''<!doctype html>
<html>
	<head>
		<meta charset="utf-8"/>
		<title>W|ASH Workbook</title>
		<link href='https://fonts.googleapis.com/css?family=PT+Sans+Caption:400,700' rel='stylesheet' type='text/css'>
		<link href='http://fonts.googleapis.com/css?family=Anonymous+Pro' rel='stylesheet' type='text/css'>
		<style>
		body {
			background-color: #E4E9EB;
			font-family: 'PT Sans Caption', sans-serif;
			margin-left: 60px;
			margin-right: 60px;
		}
		h1 {
			color: #004B63;
			margin-left: -40px;
		}
		article {
			margin-top: 2em;
			margin-bottom: 1em;
		}
		h2 {
			margin-bottom: 1em;
		}
		h3 {
			background-color: #def;
			margin-top: 0;
			margin-bottom: 0;
			padding-left: 10px;
			padding-right: 10px;
			padding-top: 1.5px;
			padding-bottom: 1.5px;
			font-size: 1.02em;
			border: 1px solid #69a;
			border-collapse: collapse;
		}
		pre {
			font-family: 'Anonymous Pro', serif;
			background-color: white;
			padding-top: .75em;
			padding-bottom: .6em;
			padding-left: 10px;
			padding-right: 10px;
			margin-top: 0;
			margin-bottom: 0;
			border-left: 1px solid #9ac;
			border-right: 1px solid #9ac;
			border-collapse: collapse;
			white-space: pre-wrap;
		}
		article > h3:nth-of-type(1) {
			border-top-left-radius: 4px;
			border-top-right-radius: 4px;
		}

		article > *:last-child {
			border-bottom: 1px solid #69a;

			border-bottom-left-radius: 4px;
			border-bottom-right-radius: 4px;
		}
		a {
			color: #004B63;
			text-decoration: none;
			border-bottom: 1px dashed black;
		}
		a:hover {
			border-bottom: 1px solid black;
		}
		</style>
	</head>
	<body>
		<h1>W|ASH Workbook</h1>
		% for query, pods in data:
			<article class="query">
				<h2><a href="http://www.wolframalpha.com/input/?i=${quote(query.encode('utf-8'))}">${query}</a></h2>
				% for name, texts in pods:
					<h3>${name}</h3>
					% for text in texts:
						<pre>${indent(text, prefix='')}</pre>
					% endfor
				% endfor
			</article>
		% endfor
	</body>
</html>''')
	fp.write(template.render(data=buffer, quote=urllib.quote, indent=indent))

def write_markdown(fp):
	template = Template('''W|ASH Workbook
==============

% for query, pods in data:
${query}
${'-' * len(query)}
	% for name, texts in pods:
${'###'} ${name}
		% for text in texts:
${indent(text)}
		% endfor

	% endfor

% endfor
''')
	fp.write(template.render(data=buffer, indent=indent))

def indent(text, prefix='    '):
	lines = text.split('\n')
	initial = min(len(line) - len(line.lstrip()) for line in lines)
	return '\n'.join(prefix + x[initial:].rstrip() for x in lines)

def clean(text):
	text = text.replace(u'\uf7d9', '=')
	return text

def wa_query(query):
	xml = requests.get(url, params=dict(input=query, appid=appid, format='plaintext')).content
	if args.verbose:
		print xml
	return BeautifulSoup(xml, 'html.parser')

def main():
	parser = argparse.ArgumentParser(description='Wolfram|Alpha interactive shell')
	parser.add_argument('-v', '--verbose', action='store_true', help='Output XML for each response')

	args = parser.parse_args()

	url = 'http://api.wolframalpha.com/v2/query'
	fn = os.path.expanduser('~/.wash.appid')
	try:
		appid = file(fn).read()
		first_run = False
	except:
		first_run = True
		print '\033[93m-- No Wolfram|Alpha app ID'
		print 'If you do not already have one, go to:'
		print '  https://developer.wolframalpha.com/portal/apisignup.html\033[0m'
		while True:
			appid = raw_input('Please enter your app ID: ').strip()
			bs = wa_query('Cody Brocious')
			print '\033[93mVerifying App ID...'
			if bs.queryresult['success'] == 'true' and bs.queryresult['error'] == 'false':
				print '\033[92mApp ID is correct\033[0m'
				with file(fn, 'w') as fp:
					fp.write(appid)
				break
			else:
				print '\033[91mApp ID is invalid\033[0m'

	if first_run:
		print
		print '\033[92mWelcome to W|ASH\033[0m'
		print '\033[93mTo get started, simply type a query here as if you are on the Wolfram|Alpha site.'
		print 'For instance, try this: the 15th prime number * 20\033[0m'
		print

	result = None

	while True:
		try:
			query = raw_input('W|A> ').strip()
		except EOFError:
			print
			break
		except KeyboardInterrupt:
			print
			continue
		readline.write_history_file(os.path.expanduser('~/.wash.history'))
		if query == '':
			continue
		elif query == 'quit' or query == 'exit':
			print '\033[91mTo quit W|ASH, press Ctrl-D\033[0m'
			continue
		elif query == 'help':
			print '\033[1m\033[92mW|ASH Help\033[0m'
			print '\033[93m - Type a query to send it to Wolfram|Alpha'
			print ' - $$ in a query will be replaced by the previous result'
			print ' - save <filename> will save the current buffer to a file as HTML or Markdown'
			print '   - To save HTML, simply add .html to the filename'
			print ' - Ctrl-D to quit\033[0m'
			print
			continue
		elif query.startswith('save '):
			fn = query[5:].strip()
			print '\033[92mSaving to', fn, '\033[0m'
			with codecs.open(fn, 'w', 'utf-8') as fp:
				if fn.lower().endswith('.html'):
					write_html(fp)
				else:
					write_markdown(fp)
			continue

		if '$$' in query:
			if result is not None:
				query = query.replace('$$', ' (%s) ' % result)
			else:
				print '\033[91m$$ in query with no previous result!\033[0m'
				print
				continue

		bs = wa_query(query)
		if bs.queryresult['success'] == 'true':
			element = (query, [])
			buffer.append(element)
			for pod in bs.find_all('pod'):
				numsubpods = int(pod['numsubpods'])
				if numsubpods == 0 or ''.join(''.join(subpod.plaintext.contents) for subpod in pod.find_all('subpod')).strip() == '':
					continue
				epod = (pod['title'], [])
				element[1].append(epod)
				print '  \033[1m\033[92m%s\033[0m' % pod['title']
				for i, subpod in enumerate(pod.find_all('subpod')):
					if len(subpod.plaintext.contents):
						text = clean('\n'.join(subpod.plaintext.contents))
						print indent(text)
						epod[1].append(text)

						if pod['title'] == 'Result':
							result = text
							if '  (' in result:
								result = result.split('  (', 1)[0]
						if i + 1 < numsubpods and numsubpods > 1 and '\n' in text:
							print
			if len(bs.find_all('pod', dict(scanner='Formula'))):
				print
				print '\033[91mThis appears to be an interactive formula.'
				print 'Results may be nonsensical.\033[0m'
		else:
			print '\033[91mQuery failed\033[0m'
			for tip in bs.find_all('tip'):
				print '\033[93m-', tip['text'], '\033[0m'
		print

if __name__=='__main__':
	main()
