import os

possible_sources = ['env', 'file', 'net']
 
def multi_crypt(mode:int, data:str, crypt_sequence:str):
   ... # TODO 

class ConfigAcceptor:
    def __init__(self, ENV_KEY:str):
        self.acceptor_data = os.environ[ENV_KEY].split(";")
        self.ENV_KEY = ENV_KEY
        self.source = self.acceptor_data[0] in possible_sources and acceptor_data[0] or None
        self.crypted_data_name = self.acceptor_data[1]
        self.decrypt_key = self.acceptor_data[2]
    def recrypt_and_get(self):
        if self.source == 'env':
            rdata = os.environ[self.crypted_data_name]
            rdata, new_key = multi_cryptor(1,rdata,self.decrypt_key)
            os.environ[self.crypted_data_name] = multi_crypt(0,rdata,new_key) 
        elif self.source == 'file':
            with open(self.crypted_data_name,'r') as f:
                rdata = "\n".join(f.readlines()) # forgot how to read all file to single string :(
                rdata, new_key = multi_cryptor(1,rdata,self.decrypt_key)
            with open(self.crypted_data_name, 'w') as f:
                f.write(multi_cryptor(0,rdata,new_key) 
        elif self.source == 'net':
            req = __import__("requests") 
            rdata = req.get(self.crypted_data_name, headers={'Authorization': self.decrypt_key}).text
            rdata, new_key = multi_cryptor(1,rdata,self.decrypt_key)
            req.patch(self.crypted_data_name, headers={'Authorization': self.decrypt_key}, json={'NewKey': new_key})
        del self # stupid self-destruction
        return rdata
