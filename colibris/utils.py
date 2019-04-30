
import builtins
import collections
import importlib
import re


def camelcase_to_underscore(s):
    return re.sub('(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', '_\\1', s).lower().strip('_')


def import_member(path):
    # The member could actually be a package/module itself
    module = import_module_or_none(path)
    if module:
        return module

    parts = path.split('.')
    module_path = '.'.join(parts[:-1])
    member_name = parts[-1]

    module = importlib.import_module(module_path)

    return getattr(module, member_name)


def import_module_or_none(path):
    # In Python < 3.6 we don't have ModuleNotFoundError
    ModuleNotFoundError = getattr(builtins, 'ModuleNotFoundError', ImportError)

    try:
        return importlib.import_module(path)

    except ModuleNotFoundError as e:
        if e.name == path:
            return None

        raise


def dict_update_rec(dest, source):
    for k, v in source.items():
        if ((k in dest) and isinstance(dest[k], dict) and
            isinstance(source[k], collections.Mapping)):

            dict_update_rec(dest[k], source[k])

        else:
            dest[k] = source[k]
