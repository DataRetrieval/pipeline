from setuptools import setup, find_packages

setup(
    name='pipeline',
    version='1.0.0',
    description='Scrapy pipeline project',
    author='Ouahib El Hanchi',
    author_email='ouahib.el.hanchi@gmail.com',
    packages=find_packages(),
    entry_points = {'scrapy': ['settings = pipeline.settings']},
    install_requires=[
        'scrapy',
        'scrapy-fake-useragent',
        'boto',
        'demjson'
        'python-dateutil'
    ],
    extras_require={
        'dev': ['flake8'],
    },
)
