import os
import hashlib
import base64
import json

import cryptography.fernet as fernet

from . import config, zero_mem
from .exceptions.data_exceptions import *


class Crypto:

    def __init__(self, password, preserve_password=False):
        # preserve password arg is used in situations like
        # wallet creation in wallet.py, where two data_store objects
        # are created in quick succession (in new_wallet cls method and __init__)

        self._fernet = fernet.Fernet(self.key_from_password(password))

        # delete password variable from memory if not preserve_password
        if not preserve_password:
            zero_mem.zeromem(password)

    @staticmethod
    def key_from_password(password, iterations=100_000):
        """ Returns a key to be used with fernet encryption"""
        b_password = password.encode('utf-8')
        b_key = hashlib.pbkdf2_hmac('sha256', b_password, b'', iterations)
        return base64.urlsafe_b64encode(b_key)

    def encrypt(self, string_):
        token = self._fernet.encrypt(string_.encode('utf-8'))
        zero_mem.zeromem(string_)
        return token.decode('utf-8')

    def decrypt(self, token):
        string = self._fernet.decrypt(token.encode('utf-8'))
        return string.decode('utf-8')


class DataStore(Crypto):

    def __init__(self, file_path, password, preserve_password=False):
        super().__init__(password, preserve_password=preserve_password)
        self.file_path = file_path
        self.json_blank_template = json.dumps(config.STANDARD_DATA_FORMAT)

        if not os.path.exists(self.file_path):
            raise ValueError(f'{self.file_path} does not exist!')

        # new file handling
        with open(self.file_path, 'r') as d:
            if d.read() == '':
                with open(self.file_path, 'w') as dw:
                    dw.write(self.encrypt(self.json_blank_template))

        if not self.check_password():
            raise IncorrectPasswordError('Entered password is incorrect')

        # Storing password hash for password validation independent of
        # this class i.e Wallet class for sensitive information
        self.write_value(PASSWORD_HASH=hashlib.sha256(password.encode('utf-8')).hexdigest())

    @property
    def _data(self):
        with open(self.file_path, 'r') as d:
            return json.loads(self.decrypt(d.read()))

    def _write_to_file(self, data):
        # if data is invalid for json.dumps it will raise exception here before file is overwritten
        json.dumps(data)
        with open(self.file_path, 'w') as d:
            d.write(self.encrypt(json.dumps(data)))

    def write_value(self, allow_new_key=False, **kwargs):
        data = self._data
        for k, v in kwargs.items():

            if k not in config.STANDARD_DATA_FORMAT and allow_new_key is False:
                raise ValueError(f'Entered key ({k}) is not valid!')

            else:
                if not isinstance(v, type(config.STANDARD_DATA_FORMAT[k])):
                    raise ValueError(f'Value ({v}) is wrong type. It must be a: '
                                     f'{type(config.STANDARD_DATA_FORMAT[k])}')

                else:
                    if k in config.SENSITIVE_DATA:
                        # if key is in sensitive data list, it will be encrypted twice
                        # to limit its exposure in ram, unencrypted
                        data[k] = self.encrypt(v)

                    else:
                        data[k] = v

            self._write_to_file(data)

    def get_value(self, key):
        if key in config.SENSITIVE_DATA:
            return self.decrypt(self._data[key.upper()])

        else:
            return self._data[key.upper()]

    def check_password(self):
        try:
            # tries to decrypt data
            _ = self._data
            return True

        except fernet.InvalidToken:
            return False

    # for use outside this class, where the password isn't actually used
    # to decrypt the file, but still needs to be verified for security
    def validate_password(self, password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest() \
               == self.get_value(key='PASSWORD_HASH')
