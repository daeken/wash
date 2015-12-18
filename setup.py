from distutils.core import setup

setup(name='WASH',
		version='0.1', 
		description='Wolfram|Alpha interactive shell', 
		author='Cody Brocious', 
		author_email='cody.brocious@gmail.com', 
		scripts=['wash'], 
		install_requires=[
			'requests',
			'beautifulsoup4', 
			'lxml'
		]
	)
