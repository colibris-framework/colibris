
import importlib
import inspect
import os
import re

from pathlib import Path
from dotenv import load_dotenv

from colibris import utils

from colibris.conf import defaultsettings
from colibris.conf import lazysettings
from colibris.conf import schemas as settings_schemas

from colibris.conf.schemas import register_settings_schema


_settings_store = {}


def _is_setting_name(name):
    # only consider public members that are all in capitals
    return re.match('^[A-Z][A-Z0-9_]*$', name)


def _set_project_package_settings():
    project_package = utils.import_module_or_none(_settings_store['PROJECT_PACKAGE_NAME'])
    if project_package is None:
        project_package = importlib.import_module('colibris')

    _settings_store.setdefault('PROJECT_PACKAGE_DIR', os.path.dirname(project_package.__file__))


def _override_setting(name, value):
    # do we have the setting corresponding to the given name?
    if name in _settings_store:
        _settings_store[name] = value
        return

    # try dictionary with items
    parts = name.split('_')
    for i in range(len(parts) - 1):
        dname = '_'.join(parts[:i + 1])
        d = _settings_store.get(dname)
        if not isinstance(d, dict):
            continue

        dkey = '_'.join(parts[i + 1:])
        d[dkey.lower()] = value  # dictionary keys are lower-case, by convention

        break

    else:
        # lastly, we simply add the new setting to the module
        _settings_store[name] = value


def _setup_default_settings():
    for name, value in inspect.getmembers(defaultsettings):
        if not _is_setting_name(name):
            continue

        _settings_store[name] = value


def _override_project_settings():
    project_settings_module = utils.import_module_or_none('settings')
    if project_settings_module is None:
        pass

    for name, value in inspect.getmembers(project_settings_module):
        if not _is_setting_name(name):
            continue

        _override_setting(name, value)


def _override_local_settings():
    settings_local_module = utils.import_module_or_none('settingslocal')
    if settings_local_module is None:
        return

    for name, value in inspect.getmembers(settings_local_module):
        if not _is_setting_name(name):
            continue

        _override_setting(name, value)


def _override_env_settings():
    load_dotenv(Path('.env.default'))
    load_dotenv(Path('.env'), override=True)

    schema_class = settings_schemas.get_all_settings_schema()
    env_vars = schema_class().load(os.environ)

    for name, value in env_vars.items():
        if value is None:
            continue

        _override_setting(name, value)


def _apply_tweaks():
    # update default log level according to DEBUG flag
    if _settings_store['LOGGING'] is defaultsettings.LOGGING and not _settings_store['DEBUG']:
        _settings_store['LOGGING']['root']['level'] = 'INFO'


def _initialize():
    _setup_default_settings()
    _override_project_settings()
    _override_local_settings()
    _override_env_settings()
    _set_project_package_settings()
    _apply_tweaks()


settings = lazysettings.LazySettings(_settings_store, _initialize)
