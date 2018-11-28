
import importlib
import re


class ClassNameException(Exception):
    def __str__(self):
        message = super().__str__()
        if not message:
            message = self.__class__.__name__

        return message


def camelcase_to_underscore(s):
    return re.sub('(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', '_\\1', s).lower().strip('_')


def import_member(path):
    parts = path.split('.')
    module_path = '.'.join(parts[:-1])
    member_name = parts[-1]

    module = importlib.import_module(module_path)

    return getattr(module, member_name)


def import_module_or_none(path):
    try:
        return importlib.import_module(path)

    except ModuleNotFoundError as e:
        if e.name == path:
            return None

        raise
