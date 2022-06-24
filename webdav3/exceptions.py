from pathlib import Path
from typing import Any, Union


class WebDavException(Exception):
    pass


class NotValid(WebDavException):
    pass


class OptionNotValid(NotValid):
    def __init__(self, name: str, value: Any, ns=""):
        self.name = name
        self.value = value
        self.ns = ns

    def __str__(self):
        return f"Option ({self.ns}{self.name}={self.value}) have invalid name or value"


class CertificateNotValid(NotValid):
    pass


class NotFound(WebDavException):
    pass


class LocalResourceNotFound(NotFound):
    def __init__(self, path: Union[str, Path]):
        self.path = path

    def __str__(self):
        return f"Local file: {self.path} not found"


class RemoteResourceNotFound(NotFound):
    def __init__(self, path: Union[str, Path]):
        self.path = path

    def __str__(self):
        return f"Remote resource: {self.path} not found"


class RemoteParentNotFound(NotFound):
    def __init__(self, path: Union[str, Path]):
        self.path = path

    def __str__(self):
        return f"Remote parent for: {self.path} not found"


class MethodNotSupported(WebDavException):
    def __init__(self, name: str, server: str):
        self.name = name
        self.server = server

    def __str__(self):
        return f"Method '{self.name}' not supported for {self.server}"


class ConnectionException(WebDavException):
    def __init__(self, exception: Exception):
        self.exception = exception

    def __str__(self):
        return self.exception.__str__()


class NoConnection(WebDavException):
    def __init__(self, hostname: str):
        self.hostname = hostname

    def __str__(self):
        return f"No connection with {self.hostname}"


# This exception left only for supporting original library interface.
class NotConnection(WebDavException):
    def __init__(self, hostname: str):
        self.hostname = hostname

    def __str__(self):
        return f"No connection with {self.hostname}"


class ResponseErrorCode(WebDavException):
    def __init__(self, url: str, code: int, message: str):
        self.url = url
        self.code = code
        self.message = message

    def __str__(self):
        return f"Request to {self.url} failed with code {self.code} and message: {self.message}"


class NotEnoughSpace(WebDavException):
    def __init__(self):
        self.message = "Not enough space on the server"

    def __str__(self):
        return self.message


class ResourceLocked(WebDavException):
    def __init__(self, path: Union[str, Path]):
        self.path = path

    def __str__(self):
        return f"Resource {self.path} locked"
