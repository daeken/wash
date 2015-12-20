from distutils.core import setup

setup(name='WASH',
		version='1.3', 
		description='Wolfram|Alpha interactive shell', 
		author='Cody Brocious', 
		author_email='cody.brocious@gmail.com', 
		scripts=['wash'], 
		install_requires=[
			'requests',
			'beautifulsoup4', 
			'mako'
		], 
		license='CC0', 
		url='https://pypi.python.org/pypi/WASH'
	)
