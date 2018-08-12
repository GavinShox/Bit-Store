import os
import pathlib
import json


DATA_DIR = os.path.join(pathlib.Path.home(), '.Bit-Store')
CONFIG_FILE = os.path.join(DATA_DIR, 'config.json')


def init():
    # creates program data dir if it doesn't exist
    if not os.path.isdir(DATA_DIR):
        os.makedirs(DATA_DIR, exist_ok=True)

    # and likewise for the config file itself
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w+') as cf:
            json.dump(DEFAULT_CONFIG, cf, indent=4, sort_keys=False)


def read_file():
    with open(CONFIG_FILE, 'r') as c:
        return json.load(c)


def reset_config_file():
    with open(CONFIG_FILE, 'w') as cf:
        json.dump(DEFAULT_CONFIG, cf, indent=4, sort_keys=False)


def write_value(key, value):
    if key not in DEFAULT_CONFIG:
        raise ValueError(f'{key} is an invalid key')

    config = read_file()
    config[key] = value

    with open(CONFIG_FILE, 'w') as cf:
        json.dump(config, cf, indent=4, sort_keys=False)


init()
_CONFIG_VARS = read_file()


DEFAULT_CONFIG = {

    'BIP32_PATHS': {
        'bip49path': "49'/0'/0'",
        'bip44path': "44'/0'/0'"
    },

    'PRICE_API_SOURCE': 'coinmarketcap',

    'BLOCKCHAIN_API_SOURCE': 'blockchain.info',

    'FIAT': 'USD',

    'UNITS': 'BTC',

    'FONT': 'verdana',

    'SPEND_UNCONFIRMED_UTXOS': False,

    'SPEND_UTXOS_INDIVIDUALLY': False
}


STANDARD_DATA_FORMAT = {
    'MNEMONIC': '',
    'XPRIV': '',
    'XPUB': '',
    'PATH': '',
    'GAP_LIMIT': 0,
    'SEGWIT': True,
    'ADDRESSES_RECEIVING': [],
    'ADDRESSES_CHANGE': [],
    'ADDRESSES_USED': [],
    'ADDRESS_BALS': {},
    'TXNS': [],
    'PRICE': 0.0,
    'WALLET_BAL': 0,
    'UNSPENT_OUTS': [],
    'PASSWORD_HASH': '',
    'ADDRESS_WIF_KEYS': {}
}


# Sensitive data must be stored as a string or dict due to limitations in data.py's
# handling of sensitive data encryption
SENSITIVE_DATA = [
    'MNEMONIC',
    'XPRIV',
    'ADDRESS_WIF_KEYS'
]


# amounts satoshis have to be multiplied by to get other units
UNIT_FACTORS = {
    'BTC': 1e8,
    'mBTC': 1e5,
    'bits': 100,
    'satoshis': 1
}


# CONFIG VARIABLES FROM FILE

BIP32_PATHS = _CONFIG_VARS['BIP32_PATHS']

PRICE_API_SOURCE = _CONFIG_VARS['PRICE_API_SOURCE']

BLOCKCHAIN_API_SOURCE = _CONFIG_VARS['BLOCKCHAIN_API_SOURCE']

FIAT = _CONFIG_VARS['FIAT']

UNITS = _CONFIG_VARS['UNITS']

FONT = _CONFIG_VARS['FONT']

SPEND_UNCONFIRMED_UTXOS = _CONFIG_VARS['SPEND_UNCONFIRMED_UTXOS']

SPEND_UTXOS_INDIVIDUALLY = _CONFIG_VARS['SPEND_UTXOS_INDIVIDUALLY']