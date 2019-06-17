
import os

from marshmallow import pre_dump, post_dump, pre_load, post_load, validates_schema
from marshmallow import fields, validate
from marshmallow import ValidationError
from marshmallow import EXCLUDE as MM_EXCLUDE
from marshmallow.schema import Schema as MMSchema, SchemaMeta as MMSchemaMeta, SchemaOpts as MMSchemaOpts

from . import ImproperlyConfigured
from . import settings
from . import logger


class ColonSeparatedStringsField(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return ''

        return ':'.join(value)

    def _deserialize(self, value, attr, data, **kwargs):
        if value is None:
            return None

        return value.split(':')


class SettingsSchemaOpts(MMSchemaOpts):
    def __init__(self, meta, **kwargs):
        super().__init__(meta, **kwargs)

        self.unknown = getattr(meta, 'unknown', MM_EXCLUDE)  # Ignore other variables, by default
        self.prefix = getattr(meta, 'prefix', '')
        self.sensible_fields = getattr(meta, 'sensible_fields', [])
        self.sensible_fields = set(self.prefix + f for f in self.sensible_fields)


class SettingsSchemaMeta(MMSchemaMeta):
    @classmethod
    def get_declared_fields(mcs, klass, cls_fields, inherited_fields, dict_cls):
        prefix = klass.opts.prefix
        cls_fields = [(prefix + n, v) for n, v in cls_fields]
        inherited_fields = [(prefix + n, v) for n, v in inherited_fields]

        return MMSchemaMeta.get_declared_fields(klass, cls_fields, inherited_fields, dict_cls)


class SettingsSchema(MMSchema, metaclass=SettingsSchemaMeta):
    OPTIONS_CLASS = SettingsSchemaOpts
    LOG_FORMAT = 'loading %s = "%s"'

    def _override_setting_rec(self, setting_dict, name, value):
        parts = name.split('_')
        for i in range(len(parts) - 1):
            root_name = '_'.join(parts[:i + 1])
            d = setting_dict.get(root_name)
            if not isinstance(d, dict):
                continue

            key = '_'.join(parts[i + 1:])
            self._override_setting_rec(d, key.lower(), value)

            break

        else:
            # Simply add the new setting to the setting dict
            setting_dict[name] = value

    def _override_setting(self, settings_dict, name, value):
        # Do we have the setting corresponding to the given name?
        if name in settings_dict:
            settings_dict[name] = value
            return

        # Recursively update dictionary with items
        self._override_setting_rec(settings_dict, name, value)

    def load(self, data, target_settings=None, log_format=LOG_FORMAT):
        if target_settings is None:
            target_settings = settings.__dict__

        try:
            loaded_settings = super().load(data)

        except ValidationError as e:
            # Pull the first erroneous field with its first error message to form an ImproperlyConfigured exception
            field, messages = list(e.messages.items())[0]
            message = messages[0]

            raise ImproperlyConfigured('{}: {}'.format(field, message))

        for name, value in sorted(loaded_settings.items()):
            if value is None:
                continue

            if name in self.opts.sensible_fields:
                logger.debug(log_format, name, '*****')

            else:
                logger.debug(log_format, name, value)

            self._override_setting(target_settings, name, value)

    def load_from_env(self, target_settings=None):
        self.load(os.environ, target_settings, log_format=self.LOG_FORMAT + ' from environment')
