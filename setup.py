
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
        'aiohttp>=3.5.0,<=3.5.4',
        'aiohttp-apispec>=1.0,<=1.3',
        # aiohttp-swagger is currently in a bad, unmaintained state, so we need to use a specific
        # commit of eLvErDe's aiohttp-swagger github repo.
        'aiohttp-swagger @ git+https://github.com/eLvErDe/aiohttp-swagger.git@39687734',
        'async-timeout',
        'marshmallow>=3.0.0b19,<=3.0.0rc7',
        'marshmallow_peewee==2.3.0',
        'peewee>=3.9',
        'peewee-migrate==1.1.6',
        'python-dotenv',
        'webargs>=5.2.0,<=5.3.2'
    ],
    url='https://github.com/colibris-framework/colibris',
    license='BSD',
    description='A lightweight framework for RESTful microservices',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='The Colibris Team',
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
