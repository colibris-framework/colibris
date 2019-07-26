import abc

from aiohttp import web, hdrs
from aiohttp_apispec import response_schema, request_schema, docs

from colibris.persist import Model


class ViewMeta(abc.ABCMeta):
    METHODS_WITH_OUTPUT = (hdrs.METH_GET, hdrs.METH_POST, hdrs.METH_PATCH, hdrs.METH_PUT)
    METHODS_WITH_INPUT = (hdrs.METH_POST, hdrs.METH_PATCH, hdrs.METH_PUT)

    def __init__(cls, name, bases, attrs):
        for http_method in hdrs.METH_ALL:
            handler_name = http_method.lower()

            if not hasattr(cls, handler_name):
                continue

            handler = getattr(cls, handler_name)
            setattr(cls, handler_name, docs()(handler))

            if getattr(cls, 'query_schema_class', None) is not None:
                setattr(cls, handler_name, request_schema(cls.query_schema_class, location='query')(handler))

            if getattr(cls, 'body_schema_class', None) is not None:
                if http_method in cls.METHODS_WITH_INPUT:
                    setattr(cls, handler_name, request_schema(cls.body_schema_class)(handler))

                if http_method in cls.METHODS_WITH_OUTPUT:
                    setattr(cls, handler_name, response_schema(cls.body_schema_class)(handler))

        if getattr(cls, 'model', None) is not None:
            assert issubclass(cls.model, Model) is True, 'The "model" should be a subclass of {}.'.format(Model)

        super().__init__(name, bases, attrs)


class View(web.View, metaclass=ViewMeta):
    authentication_required = None
    permissions = None
