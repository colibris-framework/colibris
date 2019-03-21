
import os
import re

try:
    # Speeds up load time by eliminating the pkg_resources overhead.
    import fastentrypoints

except ImportError:
    pass

from setuptools import setup, find_packages
from setuptools.command.sdist import sdist


PROJECT_PACKAGE_NAME = '__packagename__'
ROOT_DIST_FILES = ['manage.py', 'settings.py']


class SdistCommand(sdist):
    def make_release_tree(self, base_dir, files):
        super().make_release_tree(base_dir, files)

        # some files from the project root are be part
        # of the project package when using setuptools
        for file in ROOT_DIST_FILES:
            self.copy_file(file, os.path.join(base_dir, PROJECT_PACKAGE_NAME, file))


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
    description='Project description.',
    packages=find_packages(include=PROJECT_PACKAGE_NAME + '/*') + [PROJECT_PACKAGE_NAME + '.migrations'],
    package_data={
        PROJECT_PACKAGE_NAME: (package_data_rec(PROJECT_PACKAGE_NAME, 'templates') +
                               package_data_rec(PROJECT_PACKAGE_NAME, 'static'))
    },
    entry_points={
        'console_scripts': [
            '{name}={name}.manage:main'.format(name=PROJECT_PACKAGE_NAME),
        ]
    },
    cmdclass={
        'sdist': SdistCommand
    }
)
