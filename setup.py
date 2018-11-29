
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
        m = re.search("VERSION\s*=\s*'(.*?)'", f.read())
        if m:
            return m.group(1)

    return 'unknown'


setup(
    name='colibris',
    version=find_version(),
    install_requires=[
        'aiohttp',
        'aiohttp-apispec',
        'aiohttp-swagger',
        'marshmallow>=3.0.0b19',
        'marshmallow_peewee',
        'peewee',
        'peewee-migrate',
        'python-dotenv'
    ],
    url='',
    license='',
    description='A collection of libraries glued together to make writing RESTful microservices easier.',
    packages=find_packages(include='colibris/*'),
    package_data={
        'colibris': package_data_rec('colibris', 'skeleton')
    },
    entry_points={
        'console_scripts': [
            'colibris-start-project=colibris.startproject:start_project',
        ]
    }
)
