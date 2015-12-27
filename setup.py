from setuptools import setup
import sys

setup(name='WASH',
		version='1.6.2', 
		description='Wolfram|Alpha interactive shell', 
		author='Cody Brocious', 
		author_email='cody.brocious@gmail.com', 
		py_modules=['wash'], 
		entry_points=dict(
			console_scripts=[
				'wash = wash:main'
			]
		), 
		install_requires=[
			'beautifulsoup4', 
			'colorama', 
			'mako', 
			'requests',
		] + (['pyreadline', 'win_unicode_console'] if sys.platform == 'win32' else []), 
		license='CC0', 
		url='https://pypi.python.org/pypi/WASH'
	)
