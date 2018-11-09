
def wrap_one(obj):
    return obj


def wrap_many(objs, count=None, page=0, pages=1, page_size=None):
    if page_size is None:
        page_size = len(objs)

    if count is None:
        count = len(objs)

    return {
        'results': objs,
        'count': count,
        'pages': pages,
        'page': page,
        'page_size': page_size
    }


def wrap_error(code, message, details=None):
    return {
        'code': code,
        'message': message,
        'details': details
    }
