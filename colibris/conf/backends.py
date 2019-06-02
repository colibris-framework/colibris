
import logging

from colibris import utils

from . import ImproperlyConfigured


logger = logging.getLogger(__name__)

_backend_classes = []


class _BackendMixinMeta(type):
    def __init__(cls, *args, **kwargs):
        type.__init__(cls, *args, **kwargs)
        _backend_classes.append(cls)


class BackendMixin(metaclass=_BackendMixinMeta):
    _instance = None
    _class = None
    _settings = None

    @classmethod
    def configure(cls, settings):
        cls._settings = settings

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

        return cls._instance


# The base backend mixin also gets added to the backend classes list, but we don't want it there.
_backend_classes.remove(BackendMixin)
