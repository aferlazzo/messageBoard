# The MIT License (MIT)
#
# Copyright (c) 2019 Matthew Costi for Adafruit Industries
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

"""
`Request`
================================================================================


* Author(s): Matthew Costi
"""
import re


class Request:
    """
    An incoming HTTP request.
    A higher level abstraction of the raw WSGI Environ dictionary.
    """

    def __init__(self, environ):
        self._method = environ["REQUEST_METHOD"]
        self._path = environ["PATH_INFO"]
        self._query_params = self.__parse_query_params(environ.get("QUERY_STRING", ""))
        self._headers = self.__parse_headers(environ)
        self._body = environ["wsgi.input"]
        self._wsgi_environ = environ

    @property
    def method(self):
        """
        the HTTP Method Type of this request
        """
        return self._method

    @property
    def path(self):
        """
        the path this request was made to
        """
        return self._path

    @property
    def query_params(self):
        """
        Request query parameters, represented as a dictionary of
        param name to param value
        """
        return self._query_params

    @property
    def headers(self):
        """
        Request headers, represented as a dictionary of
        header name to header value
        """
        return self._headers

    @property
    def body(self):
        """
        The Request Body
        """
        return self._body

    @property
    def wsgi_environ(self):
        """
        The raw WSGI Environment dictionary representation of the request
        """
        return self._wsgi_environ

    @staticmethod
    def __parse_query_params(query_string):
        param_list = query_string.split("&")
        params = {}
        for param in param_list:
            key_val = param.split("=")
            if len(key_val) == 2:
                params[key_val[0]] = key_val[1]
        return params

    @staticmethod
    def __parse_headers(environ):
        headers = {}

        # Content Type and Content Length headers
        #  are stored in environ differently than other headers
        if "CONTENT_TYPE" in environ:
            headers["content-type"] = environ["CONTENT_TYPE"]
        if "CONTENT_LENGTH" in environ:
            headers["content-length"] = environ["CONTENT_LENGTH"]

        env_header_re = re.compile(r"HTTP_(.+)")
        for key, val in environ.items():
            header = env_header_re.match(key)
            if header:
                headers[header.group(1).replace("_", "-").lower()] = val
        return headers
