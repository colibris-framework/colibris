
import os

from setuptools import setup, find_packages


def package_data_rec(package, directory):
    paths = []
    for path, directories, filenames in os.walk(os.path.join(package, directory)):
        for filename in filenames:
            paths.append(os.path.join(path, filename)[len(package) + 1:])

    return paths


setup(
    name='colibri',
    version='0.0.1',
    install_requires=[
        'aiohttp',
        'aiohttp-apispec',
        'aiohttp-swagger',
        'marshmallow>=3.0.0b19',
        'peewee',
        'peewee-migrate',
        'python-dotenv'
    ],
    url='',
    license='',
    description='A collection of libraries glued together to make writing RESTful microservices easier.',
    packages=find_packages(include='colibri/*'),
    package_data={
        'colibri': package_data_rec('colibri', 'skeleton')
    },
    entry_points={
        'console_scripts': [
            'colibri-start-project=colibri.startproject:start_project',
        ]
    }
)
