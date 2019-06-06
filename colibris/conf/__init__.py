
import importlib
import inspect
import os
import re
import sys

from dotenv import load_dotenv

from colibris import utils

from . import defaultsettings
from . import schemas as settings_schemas


_settings_store = {}


class ImproperlyConfigured(Exception):
    pass


def _is_setting_name(name):
    # Only consider public members that are all in capitals
    return re.match('^[A-Z][A-Z0-9_]*$', name)


def _override_setting_rec(setting_dict, name, value):
    parts = name.split('_')
    for i in range(len(parts) - 1):
        root_name = '_'.join(parts[:i + 1])
        d = setting_dict.get(root_name)
        if not isinstance(d, dict):
            continue

        key = '_'.join(parts[i + 1:])
        _override_setting_rec(d, key.lower(), value)

        break

    else:
        # Simply add the new setting to the setting dict
        setting_dict[name] = value


def override_setting(name, value):
    # Do we have the setting corresponding to the given name?
    if name in _settings_store:
        _settings_store[name] = value
        return

    # Recursively update dictionary with items
    _override_setting_rec(_settings_store, name, value)


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

    _settings_store['PROJECT_PACKAGE_NAME'] = project_package_name

    project_package = importlib.import_module(project_package_name)
    _settings_store.setdefault('PROJECT_PACKAGE_DIR', os.path.dirname(project_package.__file__))


def _setup_default_settings():
    for name, value in inspect.getmembers(defaultsettings):
        if not _is_setting_name(name):
            continue

        _settings_store[name] = value


def _override_project_settings():
    project_settings_module = utils.import_module_or_none('settings')
    if project_settings_module is None:
        # Try settings module from project package
        project_settings_path = '{}.settings'.format(_settings_store['PROJECT_PACKAGE_NAME'])
        project_settings_module = utils.import_module_or_none(project_settings_path)
        if project_settings_module is None:
            return

    for name, value in inspect.getmembers(project_settings_module):
        if not _is_setting_name(name):
            continue

        override_setting(name, value)


def _override_local_settings():
    settings_local_module = utils.import_module_or_none('settingslocal')
    if settings_local_module is None:
        return

    for name, value in inspect.getmembers(settings_local_module):
        if not _is_setting_name(name):
            continue

        override_setting(name, value)


def _override_env_settings():
    schema_class = settings_schemas.get_all_settings_schema()

    try:
        env_vars = schema_class().load(os.environ)

    except settings_schemas.ValidationError as e:
        # Pull the first erroneous field with its first error message to form an ImproperlyConfigured exception
        field, messages = list(e.messages.items())[0]
        message = messages[0]

        raise ImproperlyConfigured('{}: {}'.format(field, message))

    for name, value in env_vars.items():
        if value is None:
            continue

        override_setting(name, value)


def _apply_tweaks():
    # Update default log level according to DEBUG flag
    if _settings_store['LOGGING'] is defaultsettings.LOGGING and not _settings_store['DEBUG']:
        _settings_store['LOGGING']['root']['level'] = 'INFO'


def setup():
    load_dotenv('.env.default')
    load_dotenv('.env', override=True)

    _setup_default_settings()
    _setup_project_package()
    _override_project_settings()
    _override_local_settings()
    _override_env_settings()
    _apply_tweaks()
