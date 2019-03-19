
from aiohttp.web import Response

from colibris import api
from colibris import template


def get_object_or_404(model, pk, select_related=None):
    select_related = set(select_related or ())

    try:
        q = model.select(model, *select_related).where(model._meta.primary_key == pk)
        for m in select_related:
            q = q.join(m)

        return q.get()

    except model.DoesNotExist:
        raise api.ModelNotFoundException(model)


def html_response(body=None, status=200, reason=None, headers=None, content_type='text/html'):
    return Response(body=body, status=status, reason=reason,
                    headers=headers, content_type=content_type)


def html_response_template(template_name=None, status=200, reason=None, headers=None, content_type='text/html',
                           **context):

    return html_response(body=template.render(template_name, **context),
                         status=status, reason=reason, headers=headers, content_type=content_type)
