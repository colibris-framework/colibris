
from colibris import api


def get_object_or_404(model, pk):
    try:
        return model.select().where(model._meta.primary_key == pk).get()

    except model.DoesNotExist:
        raise api.NotFoundException(model)
