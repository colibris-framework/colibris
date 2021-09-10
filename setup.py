
import os
import re

from setuptools import setup, find_packages


def package_data_rec(package, directory):
    paths = []
    for path, directories, filenames in os.walk(os.path.join(package, directory)):
        for filename in filenames:
            paths.append(os.path.join(path, filename)[len(package) + 1:])

    return paths


def find_version():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'colibris', '__init__.py')) as f:
        m = re.search(r"VERSION\s*=\s*'(.*?)'", f.read())
        if m:
            return m.group(1)

    return 'unknown'


setup(
    name='colibris',
    version=find_version(),
    install_requires=[
        'aiohttp>=3.5.0,<=3.7.4',
        'aiohttp-apispec>=1.5',
        'apispec>=3.0.0,<4.0.0',
        'async-timeout<4.0',
        'marshmallow>=3.0.0b19,<3.8',
        'marshmallow_peewee>=2.3.0,<3.1',
        'peewee>=3.9',
        'peewee-moves>=2.1.0,<3.0',
        'python-dotenv',
        'webargs>=5.2.0,<6.0'
    ],
    url='https://github.com/colibris-framework/colibris',
    license='BSD',
    description='A lightweight framework for RESTful microservices',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='The Colibris Team',
    packages=find_packages(include='colibris/*'),
    package_data={
        'colibris': (package_data_rec('colibris', 'skeleton') +
                     package_data_rec('colibris', 'docs'))
    },
    entry_points={
        'console_scripts': [
            'colibris-start-project=colibris.startproject:start_project',
        ]
    }
)
