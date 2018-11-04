
import re


def camelcase_to_underscore(input):
    return re.sub('(((?<=[a-z])[A-Z])|([A-Z](?![A-Z]|$)))', '_\\1', input).lower().strip('_')
