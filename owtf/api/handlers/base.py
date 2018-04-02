"""
owtf.api.handlers.base
~~~~~~~~~~~~~~~~~~~~~~

"""
import json
import uuid
try:
    from http.client import responses
except ImportError:
    from httplib import responses

from tornado.escape import url_escape
from tornado.web import RequestHandler

from owtf.api.handlers.auth import auth_header_pat
from owtf.settings import SERVER_PORT, FILE_SERVER_PORT, SERVER_ADDR, SESSION_COOKIE_NAME
from owtf.utils.http import url_path_join

__all__ = ['APIRequestHandler', 'FileRedirectHandler', 'UIRequestHandler']


class APIRequestHandler(RequestHandler):

    def initialize(self):
        """
        - Set Content-type for JSON
        """
        self.session = self.application.session
        self.set_header("Content-Type", "application/json")

    def write(self, chunk):
        if isinstance(chunk, list):
            super(APIRequestHandler, self).write(json.dumps(chunk))
        else:
            super(APIRequestHandler, self).write(chunk)

    def success(self, data):
        """When an API call is successful, the JSend object is used as a simple
        envelope for the results, using the data key.

        :type  data: A JSON-serializable object
        :param data: Acts as the wrapper for any data returned by the API
            call. If the call returns no data, data should be set to null.
        """
        self.write({'status': 'success', 'data': data})
        self.finish()

    def fail(self, data):
        """There was a problem with the data submitted, or some pre-condition
        of the API call wasn't satisfied.

        :type  data: A JSON-serializable object
        :param data: Provides the wrapper for the details of why the request
            failed. If the reasons for failure correspond to POST values,
            the response object's keys SHOULD correspond to those POST values.
        """
        self.write({'status': 'fail', 'data': data})
        self.finish()

    def error(self, message, data=None, code=None):
        """An error occurred in processing the request, i.e. an exception was
        thrown.

        :type  data: A JSON-serializable object
        :param data: A generic container for any other information about the
            error, i.e. the conditions that caused the error,
            stack traces, etc.
        :type  message: A JSON-serializable object
        :param message: A meaningful, end-user-readable (or at the least
            log-worthy) message, explaining what went wrong
        :type  code: int
        :param code: A numeric code corresponding to the error, if applicable
        """
        result = {'status': 'error', 'message': message}
        if data:
            result['data'] = data
        if code:
            result['code'] = code
        self.write(result)
        self.finish()

    def write_error(self, status_code, **kwargs):
        """Write JSON errors instead of HTML"""
        exc_info = kwargs.get('exc_info')
        message = ''
        status_message = responses.get(status_code, 'Unknown Error')
        if exc_info:
            exception = exc_info[1]
            # get the custom message, if defined
            try:
                message = exception.log_message % exception.args
            except Exception:
                pass

            # construct the custom reason, if defined
            reason = getattr(exception, 'reason', '')
            if reason:
                status_message = reason
        self.write(json.dumps({
            'status': status_code,
            'message': message or status_message,
        }))

    def get_auth_token(self):
        """Get the authorization token from Authorization header"""
        auth_header = self.request.headers.get('Authorization', '')
        match = auth_header_pat.match(auth_header)
        if not match:
            return None
        return match.group(1)

    def check_referer(self):
        """Check Origin for cross-site API requests.
        Copied from WebSocket with changes:
        - allow unspecified host/referer (e.g. scripts)
        """
        host = self.request.headers.get("Host")
        referer = self.request.headers.get("Referer")

        # If no header is provided, assume it comes from a script/curl.
        # We are only concerned with cross-site browser stuff here.
        if not host:
            self.application.log.warning("Blocking API request with no host")
            return False
        if not referer:
            self.application.log.warning("Blocking API request with no referer")
            return False

        host_path = url_path_join(host, SERVER_ADDR)
        referer_path = referer.split('://', 1)[-1]
        if not (referer_path + '/').startswith(host_path):
            self.application.log.warning("Blocking Cross Origin API request.  Referer: %s, Host: %s", referer,
                                         host_path)
            return False
        return True


class UIRequestHandler(RequestHandler):

    def reverse_url(self, name, *args):
        url = super(UIRequestHandler, self).reverse_url(name, *args)
        url = url.replace('?', '')
        return url.split('None')[0]

    def _set_cookie(self, key, value, encrypted=True, **overrides):
        """Setting any cookie should go through here
        if encrypted use tornado's set_secure_cookie,
        otherwise set plaintext cookies.
        """
        # tornado <4.2 have a bug that consider secure==True as soon as
        # 'secure' kwarg is passed to set_secure_cookie
        kwargs = {
            'httponly': True,
        }
        if self.request.protocol == 'https':
            kwargs['secure'] = True
        kwargs['domain'] = SERVER_ADDR
        kwargs.update(self.settings.get('cookie_options', {}))
        kwargs.update(overrides)

        if encrypted:
            set_cookie = self.set_secure_cookie
        else:
            set_cookie = self.set_cookie

        self.application.log.debug("Setting cookie %s: %s", key, kwargs)
        set_cookie(key, value, **kwargs)

    def _set_user_cookie(self, user, server):
        self.application.log.debug("Setting cookie for %s: %s", user.name, server.cookie_name)
        self._set_cookie(
            server.cookie_name,
            user.cookie_id,
            encrypted=True,
            path=server.base_url,
        )

    def get_session_cookie(self):
        """Get the session id from a cookie
        Returns None if no session id is stored
        """
        return self.get_cookie(SESSION_COOKIE_NAME, None)

    def set_session_cookie(self):
        """Set a new session id cookie
        new session id is returned
        Session id cookie is *not* encrypted,
        so other services on this domain can read it.
        """
        session_id = uuid.uuid4().hex
        self._set_cookie(SESSION_COOKIE_NAME, session_id, encrypted=False)
        return session_id

    @property
    def template_context(self):
        user = self.get_current_user()
        return dict(user=user)


class FileRedirectHandler(RequestHandler):
    SUPPORTED_METHODS = ['GET']

    def get(self, file_url):
        output_files_server = "{}://{}/".format(self.request.protocol,
                                                self.request.host.replace(str(SERVER_PORT), str(FILE_SERVER_PORT)))
        redirect_file_url = output_files_server + url_escape(file_url, plus=False)
        self.redirect(redirect_file_url, permanent=True)
