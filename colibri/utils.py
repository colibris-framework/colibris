
import importlib
import re


def camelcase_to_underscore(s):
    return re.sub('(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', '_\\1', s).lower().strip('_')


def import_member(path):
    parts = path.split('.')
    module_path = '.'.join(parts[:-1])
    member_name = parts[-1]

    module = importlib.import_module(module_path)

    return getattr(module, member_name)
