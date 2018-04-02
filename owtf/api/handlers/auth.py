"""
owtf.api.handlers.auth
~~~~~~~~~~~~~~~~~~~~~~

"""
import re

from tornado.escape import url_escape

from owtf.api.handlers.base import UIRequestHandler, APIRequestHandler

# pattern for the authentication token header
auth_header_pat = re.compile(r'^(?:token|bearer)\s+([^\s]+)$', flags=re.IGNORECASE)


class TokenAPIHandler(APIRequestHandler):
    pass


class LogoutHandler(UIRequestHandler):
    """Log a user out by clearing their login cookie."""

    def get(self):
        user = self.get_current_user()
        #TODO


class LoginHandler(UIRequestHandler):
    """Render the login page."""

    def _render(self, login_error=None, username=None):
        return self.render(
            'login.html',
            next=url_escape(self.get_argument('next', default='')),
            username=username,
            login_error=login_error,
        )
