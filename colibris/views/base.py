import abc

from aiohttp import web, hdrs
from aiohttp_apispec import response_schema, request_schema, docs

from colibris.persist import Model


class ViewMeta(abc.ABCMeta):
    def __init__(cls, name, bases, attrs):
        for http_method in hdrs.METH_ALL:
            method_name = http_method.lower()

            if not hasattr(cls, method_name):
                continue

            handler = getattr(cls, method_name)
            setattr(cls, method_name, docs()(handler))

            if getattr(cls, 'query_schema_class', None) is not None:
                setattr(cls, method_name, request_schema(cls.query_schema_class, location='query')(handler))

        if getattr(cls, 'model', None) is not None:
            assert issubclass(cls.model, Model) is True, 'The "model" should be a subclass of {}.'.format(Model)

        if getattr(cls, 'body_schema_class', None) is not None:
            if hasattr(cls, 'get'):
                cls.get = response_schema(cls.body_schema_class)(cls.get)

            if hasattr(cls, 'post'):
                cls.post = request_schema(cls.body_schema_class)(response_schema(cls.body_schema_class)(cls.post))

            if hasattr(cls, 'put'):
                cls.put = request_schema(cls.body_schema_class)(response_schema(cls.body_schema_class)(cls.put))

            if hasattr(cls, 'patch'):
                cls.patch = request_schema(cls.body_schema_class)(response_schema(cls.body_schema_class)(cls.patch))

        super().__init__(name, bases, attrs)


class View(web.View, metaclass=ViewMeta):
    pass
