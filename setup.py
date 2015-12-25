from setuptools import setup

setup(name='WASH',
		version='1.6', 
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
			'requests',
			'beautifulsoup4', 
			'mako'
		], 
		license='CC0', 
		url='https://pypi.python.org/pypi/WASH'
	)
