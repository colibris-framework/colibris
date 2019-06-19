
import os
import re

try:
    # Speeds up load time by eliminating the pkg_resources overhead.
    import fastentrypoints

except ImportError:
    pass

from setuptools import setup, find_packages


PROJECT_PACKAGE_NAME = '__packagename__'
PROJECT_NAME = '__projectname__'


def package_data_rec(package, directory):
    paths = []
    for path, directories, filenames in os.walk(os.path.join(package, directory)):
        for filename in filenames:
            paths.append(os.path.join(path, filename)[len(package) + 1:])

    return paths


def find_version():
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), PROJECT_PACKAGE_NAME, '__init__.py')) as f:
        m = re.search(r"VERSION\s*=\s*'(.*?)'", f.read())
        if m:
            return m.group(1)

    return 'unknown'


setup(
    name=PROJECT_PACKAGE_NAME,
    version=find_version(),
    install_requires=[
        'colibris'
    ],
    url='',
    license='',
    description='Project description',
    packages=find_packages(include=PROJECT_PACKAGE_NAME + '/*'),
    package_data={
        PROJECT_PACKAGE_NAME: (package_data_rec(PROJECT_PACKAGE_NAME, 'templates') +
                               package_data_rec(PROJECT_PACKAGE_NAME, 'static') +
                               ['.env.default'])
    },
    entry_points={
        'console_scripts': [
            '{project_name}={package_name}.manage:main'.format(project_name=PROJECT_NAME,
                                                               package_name=PROJECT_PACKAGE_NAME),
        ]
    }
)
