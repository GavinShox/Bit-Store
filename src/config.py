import pathlib
import os


DATA_DIR = os.path.join(pathlib.Path.home(), '.BTC-WALLET')

###############################################################################

STANDARD_DATA_FORMAT = {
        'MNEMONIC': '',
        'XPRIV': '',
        'XPUB': '',
        'PATH': '',
        'GAP_LIMIT': 0,
        'SEGWIT': bool,
        'ADDRESSES_RECEIVING': [],
        'ADDRESSES_CHANGE': [],
        'ADDRESSES_USED': [],
}

SENSITIVE_DATA = [
        'MNEMONIC',
        'XPRIV',
]

###############################################################################

BIP32_PATHS = {
        'bip49path': "49'/0'/0'",
        'bip44path': "44'/0'/0'"
}
