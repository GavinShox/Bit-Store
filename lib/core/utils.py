import os
import decimal
from hashlib import sha256
from functools import wraps
from threading import Thread


def atomic_file_write(data: str, file_path: str):
    """ atomically write data (string) to a file """

    tmp_file = file_path + '.tmp'
    with open(tmp_file, 'w') as f:
        f.write(data)
        f.flush()
        os.fsync(f.fileno())

    os.replace(tmp_file, file_path)


def threaded(func=None, daemon=False):
    """ wrapper that returns a thread handle with its target set to wrapped function """
    def decorator(func_):

        @wraps(func_)
        def wrapped(*args, **kwargs):
            t = Thread(target=func_, args=args, kwargs=kwargs, daemon=daemon)
            t.start()
            return t

        return wrapped

    if func:
        return decorator(func)

    return decorator


def decode_base58(bc, length):
    digits58 = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    n = 0
    for char in bc:
        n = n * 58 + digits58.index(char)
    return n.to_bytes(length, 'big')


def check_bc(bc):
    """ function that validates a btc address """
    try:
        if isinstance(bc, list):
            valid_list = []

            for a in bc:
                bcbytes = decode_base58(a, 25)
                valid_list.append(bcbytes[-4:] == sha256(sha256(bcbytes[:-4]).digest()).digest()[:4])

            return all(valid_list)


        else:
            bcbytes = decode_base58(bc, 25)
            return bcbytes[-4:] == sha256(sha256(bcbytes[:-4]).digest()).digest()[:4]
    except Exception:
        return False


def float_to_str(float_):
    """ Convert the given float to a string, without scientific notation """
    with decimal.localcontext() as ctx:
        d1 = ctx.create_decimal(repr(float_))
        return format(d1, 'f')
