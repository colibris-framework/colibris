
from colibris.conf.backends import BackendMixin

from .exceptions import NoSuchAccount


_ACCOUNT_ACTION_LOGIN = 'login'
_ACCOUNT_ACTION_LOGIN_PERSISTENT = 'login_persistent'
_ACCOUNT_ACTION_LOGOUT = 'logout'

_REQUEST_ACCOUNT_ACTION_ITEM_NAME = 'account_action'


class AuthenticationBackend(BackendMixin):
    def extract_auth_data(self, request):
        raise NotImplementedError

    def lookup_account(self, identity):
        raise NotImplementedError

    def verify_identity(self, request, account, auth_data):
        # To be overridden if identity verification is needed.
        pass

    def authenticate(self, request):
        auth_data = self.extract_auth_data(request)
        account = self.lookup_account(auth_data)
        if account is None:
            raise NoSuchAccount()

        self.verify_identity(request, account, auth_data)

        return account

    def login(self, request, persistent):
        if persistent:
            request[_REQUEST_ACCOUNT_ACTION_ITEM_NAME] = _ACCOUNT_ACTION_LOGIN_PERSISTENT

        else:
            request[_REQUEST_ACCOUNT_ACTION_ITEM_NAME] = _ACCOUNT_ACTION_LOGIN

    def logout(self, request):
        request[_REQUEST_ACCOUNT_ACTION_ITEM_NAME] = _ACCOUNT_ACTION_LOGOUT

    def prepare_login_response(self, response, account, persistent):
        return response

    def prepare_logout_response(self, response):
        return response

    def process_request(self, request):
        return request

    def process_response(self, request, response):
        from . import get_account

        # Handle logins and logouts
        account_action = request.get(_REQUEST_ACCOUNT_ACTION_ITEM_NAME)
        if account_action:
            account = get_account(request)
            if account_action == _ACCOUNT_ACTION_LOGIN:
                response = self.prepare_login_response(response, account, persistent=False)

            elif account_action == _ACCOUNT_ACTION_LOGIN_PERSISTENT:
                response = self.prepare_login_response(response, account, persistent=True)

            elif account_action == _ACCOUNT_ACTION_LOGOUT:
                response = self.prepare_logout_response(response)

        return response
