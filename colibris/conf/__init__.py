
import importlib
import inspect
import logging.config
import logging.handlers
import os
import re
import sys

from dotenv import load_dotenv

from colibris import utils

from . import settings


ENV_DEFAULT = '.env.default'

logger = logging.getLogger(__name__)


class ImproperlyConfigured(Exception):
    pass


_default_logging_dict = settings.LOGGING  # Remember original logging config to tell if changed
_logging_memory_handler = None


def _is_setting_name(name):
    # Only consider public members that are all in capitals
    return re.match('^[A-Z][A-Z0-9_]*$', name)


def _setup_project_package():
    # Autodetect project package from main script path
    main_script = sys.argv[0]
    project_package_name = None
    if main_script.endswith('manage.py'):  # Using manage.py
        main_script = os.path.realpath(main_script)
        project_package_name = os.path.basename(os.path.dirname(main_script))
        sys.path.insert(0, os.path.dirname(os.path.dirname(main_script)))

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


def _setup_env():
    # Try to load a default env file from the project package
    path = os.path.join(settings.PROJECT_PACKAGE_DIR, ENV_DEFAULT)
    if os.path.exists(path):
        load_dotenv(path)

    # Try to load an env file from the current directory
    load_dotenv('.env', override=True)


def _setup_project_settings():
    project_settings_path = '{}.settings'.format(settings.PROJECT_PACKAGE_NAME)
    project_settings_module = utils.import_module_or_none(project_settings_path)
    if project_settings_module is None:
        return

    for name, value in inspect.getmembers(project_settings_module):
        if not _is_setting_name(name):
            continue

        setattr(settings, name, value)


def _setup_logging():
    # Update default log level according to DEBUG flag
    if settings.LOGGING is _default_logging_dict and not settings.DEBUG:
        settings.LOGGING['root']['level'] = 'INFO'

    logging_config = dict(settings.LOGGING)
    logging_config['disable_existing_loggers'] = False
    utils.dict_update_rec(logging_config, settings.LOGGING_OVERRIDES)

    logging.config.dictConfig(logging_config)

    # Handle logs emitted before logging setup
    if _logging_memory_handler:
        _logging_memory_handler.setTarget(logging.getLogger())
        _logging_memory_handler.flush()


def get_logging_memory_handler():
    global _logging_memory_handler

    if _logging_memory_handler is None:
        _logging_memory_handler = logging.handlers.MemoryHandler(capacity=1e6, flushLevel=logging.CRITICAL)

    return _logging_memory_handler


def setup():
    _setup_project_package()
    _setup_env()
    _setup_project_settings()
    _setup_logging()
