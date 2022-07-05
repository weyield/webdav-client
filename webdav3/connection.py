from os.path import exists
from pathlib import Path
from typing import Any, Dict, Optional, Union

from webdav3.exceptions import *
from webdav3.urn import Urn


class ConnectionSettings:
    def is_valid(self):
        """
        Method checks is settings are valid
        :return: True if settings are valid otherwise False
        """
        pass

    def valid(self):
        try:
            self.is_valid()
        except OptionNotValid:
            return False
        else:
            return True


class WebDAVSettings(ConnectionSettings):
    ns = "webdav:"
    prefix = "webdav_"
    keys = {'hostname', 'login', 'password', 'token', 'root', 'cert_path', 'key_path', 'recv_speed', 'send_speed',
            'verbose', 'disable_check', 'override_methods', 'timeout', 'chunk_size'}

    def __init__(self, options: Dict[str, Any]):
        self.hostname: Optional[str] = None
        self.login: Optional[str] = None
        self.password: Optional[str] = None
        self.token: Optional[str] = None
        self.root: Optional[str] = None
        self.cert_path: Optional[Union[str, Path]] = None
        self.key_path: Optional[Union[str, Path]] = None
        self.recv_speed = None
        self.send_speed = None
        self.verbose = None
        self.disable_check = False
        self.override_methods = {}
        self.timeout: int = 30
        self.chunk_size: int = 65536

        self.options = dict()

        for key in self.keys:
            value = options.get(key, '')
            if not (self.__dict__[key] and not value):
                self.options[key] = value
                self.__dict__[key] = value

        self.root = Urn(self.root).quote() if self.root else ''
        self.root = self.root.rstrip(Urn.separate)
        self.hostname = self.hostname.rstrip(Urn.separate)

    def is_valid(self):
        if self.hostname is None:
            raise OptionNotValid(name="hostname", value=self.hostname, ns=self.ns)

        if self.cert_path is not None and not exists(self.cert_path):
            raise OptionNotValid(name="cert_path", value=self.cert_path, ns=self.ns)

        if self.key_path is not None and not exists(self.key_path):
            raise OptionNotValid(name="key_path", value=self.key_path, ns=self.ns)

        if self.key_path is not None and not self.cert_path:
            raise OptionNotValid(name="cert_path", value=self.cert_path, ns=self.ns)

        if self.password is not None and self.login is None:
            raise OptionNotValid(name="login", value=self.login, ns=self.ns)
        return True
