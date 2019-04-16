
from colibris import authentication
from colibris.authentication.exceptions import NoSuchAccount, IdentityVerificationFailed


_ACCOUNT_ACTION_LOGIN = 'login'
_ACCOUNT_ACTION_LOGIN_PERSISTENT = 'login_persistent'
_ACCOUNT_ACTION_LOGOUT = 'logout'

_REQUEST_ACCOUNT_ACTION_ITEM_NAME = 'account_action'


class AuthenticationBackend:
    def extract_auth_data(self, request):
        raise NotImplementedError

    def lookup_account(self, identity):
        raise NotImplementedError

    def verify_identity(self, request, account, auth_data):
        raise NotImplementedError

    def authenticate(self, request):
        identity, auth_data = self.extract_auth_data(request)
        account = self.lookup_account(identity)
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
        # Handle logins and logouts
        account_action = request.get(_REQUEST_ACCOUNT_ACTION_ITEM_NAME)
        if account_action:
            account = authentication.get_account(request)
            if account_action == _ACCOUNT_ACTION_LOGIN:
                response = self.prepare_login_response(response, account, persistent=False)

            elif account_action == _ACCOUNT_ACTION_LOGIN_PERSISTENT:
                response = self.prepare_login_response(response, account, persistent=True)

            elif account_action == _ACCOUNT_ACTION_LOGOUT:
                response = self.prepare_logout_response(response)

        return response


class NullBackend(AuthenticationBackend):
    _DUMMY_ACCOUNT = {}

    def __init__(self, **kwargs):
        pass

    def extract_auth_data(self, request):
        return None, None

    def lookup_account(self, identity):
        return self._DUMMY_ACCOUNT

    def verify_identity(self, request, account, auth_data):
        pass

    def authenticate(self, request):
        return self._DUMMY_ACCOUNT
