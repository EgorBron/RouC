"""MIT License

Copyright (c) 2022 RouC Team, EgorBron, Blusutils

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# In progress

import os
import typing
import random

possible_sources = ['env', 'file', 'net']
 
def multi_cryptor(mode:int, data:str, crypt_sequence:str) -> typing.Tuple[str, typing.Union[str, None]]:
    """Crypts data
    Args:
        mode (int): Mode: 0 is "decrypt", 1 is "encrypt"
        data (str): Data to be crypted
        crypt_sequence (str): Crypt sequence to be used
    Raises:
        ValueError: if mode is not 0 or 1
    Returns:
        typing.Tuple[str, typing.Union[str, None]]: A tuple with encrypted/decrypted data and newly generated crypt sequence (only when decrypting).
    """
    codings = {
        "u": 'utf-8',
        #"c": 'cp1251',
        "a": "1256"
    }
    en_to_ru = dict(zip(map(ord, "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
                            'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'),
                            "йцукенгшщзхъфывапролджэячсмитьбю.ё"
                            'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'))
    ru_to_en = dict(zip(map(ord, "йцукенгшщзхъфывапролджэячсмитьбю.ё"
                            'ЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ,Ё'),
                            "qwertyuiop[]asdfghjkl;'zxcvbnm,./`"
                            'QWERTYUIOP{}ASDFGHJKL:"ZXCVBNM<>?~'))
    data = data.translate(en_to_ru) if mode == 0 else data
    data:typing.Union[str, bytes] = data
    if mode == 0:
        crypt_sequence = 'u'+crypt_sequence if not crypt_sequence.startswith('u') else crypt_sequence
    elif mode == 1:
        crypt_sequence = crypt_sequence[::-1]+'u' if not crypt_sequence.endswith('u') else crypt_sequence
    else: raise ValueError("Mode is not equal to 0 (decrypt) or 1 (encrypt)")
    for coding in crypt_sequence:
        data = data.encode(codings[coding]) if isinstance(data, str) else data.decode(codings[coding])
    data = data.translate(ru_to_en) if mode == 1 else data
    return data, "".join([random.choice(list(codings.keys())) for _ in range(len(crypt_sequence))]) if mode == 1 else None

class ConfigAcceptor:
    def __init__(self, ENV_KEY:str):
        self.ENV_KEY = ENV_KEY
        self.refresh_key()
    def refresh_key(self):
        self.acceptor_data = os.environ[self.ENV_KEY].split(";")
        self.source = self.acceptor_data[0] in possible_sources and self.acceptor_data[0] or None
        self.crypted_data_name = self.acceptor_data[1]
        self.decrypt_key = self.acceptor_data[2]
    def recrypt_and_get(self):
        self.refresh_key()
        def upd_key(new_key):
            self.decrypt_key = new_key
            changed_env_key = os.environ[self.ENV_KEY].split(";")
            changed_env_key[2] = new_key
            os.environ[self.ENV_KEY] = ";".join(changed_env_key)
        if self.source == 'env':
            rdata = os.environ[self.crypted_data_name]
            rdata, new_key = multi_cryptor(1,rdata,self.decrypt_key)
            os.environ[self.crypted_data_name] = multi_cryptor(0,rdata,new_key) 
            upd_key(new_key)
        elif self.source == 'file':
            with open(self.crypted_data_name,'r') as f:
                rdata = "\n".join(f.readlines()) # forgot how to read all file to single string :(
                rdata, new_key = multi_cryptor(1,rdata,self.decrypt_key)
                upd_key(new_key)
            with open(self.crypted_data_name, 'w') as f:
                f.write(multi_cryptor(0,rdata,new_key))
        elif self.source == 'net':
            req = __import__("requests") 
            rdata = req.get(self.crypted_data_name, headers={'Authorization': self.decrypt_key}).text
            rdata, new_key = multi_cryptor(1,rdata,self.decrypt_key)
            req.patch(self.crypted_data_name, headers={'Authorization': self.decrypt_key}, json={'NewKey': new_key})
            upd_key(new_key)
        del self # stupid self-destruction
        return rdata
