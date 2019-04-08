
from .exceptions import *


REQUEST_ACCOUNT_ITEM_NAME = 'account'


def get_account(request):
    return request.get(REQUEST_ACCOUNT_ITEM_NAME)
