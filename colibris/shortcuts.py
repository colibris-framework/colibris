
from colibris import api


def get_object_or_404(model, pk, select_related=None):
    select_related = set(select_related or ())

    try:
        q = model.select(model, *select_related).where(model._meta.primary_key == pk)
        for m in select_related:
            q = q.join(m)

        return q.get()

    except model.DoesNotExist:
        raise api.ModelNotFoundException(model)
