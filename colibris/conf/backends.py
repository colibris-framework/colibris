
import logging

from colibris import utils

from . import ImproperlyConfigured


logger = logging.getLogger(__name__)


class BackendMixin:
    _instance = None
    _class = None
    _settings = None

    @classmethod
    def configure(cls, settings):
        cls._settings = settings
        cls._instance = None

        try:
            backend_path = settings.pop('backend')

        except KeyError:
            return  # Backend class not specified

        cls._class = utils.import_member(backend_path)
        logger.debug('%s: using class %s', cls.__name__, backend_path)

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            if cls._settings is None:
                raise ImproperlyConfigured('{} has not been configured'.format(cls.__name__))

            if cls._class is None:
                raise ImproperlyConfigured('class for {} has not been specified'.format(cls.__name__))

            cls._instance = cls._class(**cls._settings)
            cls._instance.on_create()

        return cls._instance

    @classmethod
    def is_configured(cls):
        return cls._settings is not None

    @classmethod
    def is_enabled(cls):
        return cls._class is not None

    @classmethod
    def is_created(cls):
        return cls._instance is not None

    def on_create(self):
        pass
