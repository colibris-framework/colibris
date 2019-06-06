
import importlib
import inspect
import os
import re
import sys

from dotenv import load_dotenv

from colibris import utils

from . import settings
from . import schemas as settings_schemas


_default_logging_dict = settings.LOGGING  # Remember original logging config to tell if changed


class ImproperlyConfigured(Exception):
    pass


def _is_setting_name(name):
    # Only consider public members that are all in capitals
    return re.match('^[A-Z][A-Z0-9_]*$', name)


def _setup_project_package():
    # Autodetect project package from main script path
    main_script = sys.argv[0]
    project_package_name = None
    if main_script.endswith('manage.py'):  # using manage.py
        main_script = os.path.realpath(main_script)
        project_package_name = os.path.basename(os.path.dirname(main_script))
        project_package_name = re.sub('[^a-z0-9_]', '', project_package_name).lower()

    else:  # Using a setuptools console script wrapper
        with open(main_script, 'rt') as main_module_file:
            main_content = main_module_file.read()
            # Try simple wrapper
            m = re.search(r'from (\w+).manage import main', main_content)
            if m:
                project_package_name = m.group(1)
            
            else:
                # pkg_resources kind wrapper
                m = re.search(r"load_entry_point\('(\w+)==", main_content)
                if m:
                    project_package_name = m.group(1)
    
    if project_package_name is None:
        raise ImproperlyConfigured('could not identify project package name')

    settings.PROJECT_PACKAGE_NAME = project_package_name

    project_package = importlib.import_module(project_package_name)
    settings.PROJECT_PACKAGE_DIR = os.path.dirname(project_package.__file__)


def _setup_project_settings():
    project_settings_path = '{}.settings'.format(settings.PROJECT_PACKAGE_NAME)
    project_settings_module = utils.import_module_or_none(project_settings_path)
    if project_settings_module is None:
        return

    for name, value in inspect.getmembers(project_settings_module):
        if not _is_setting_name(name):
            continue

        setattr(settings, name, value)


def _apply_tweaks():
    # Update default log level according to DEBUG flag
    if settings.LOGGING is _default_logging_dict and not settings.DEBUG:
        settings.LOGGING['root']['level'] = 'INFO'


def setup():
    load_dotenv('.env.default')
    load_dotenv('.env', override=True)

    _setup_project_package()
    _setup_project_settings()
    _apply_tweaks()
