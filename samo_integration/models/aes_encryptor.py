import base64
import hashlib
from datetime import datetime

from Crypto.Cipher import AES
from pkcs7 import PKCS7Encoder


class Main:
    '''
    AES ENCRYPT , dedicated for SAMO , all datas are preset
    COPY right @Nizar Aouili :D !!
    '''

    def __init__(self, key, password):
        self.key = key or 'c132b4bc6a48e054770af7b1f925d95c'
        self.password = password or 'St@25648'

    def getsalt(self):
        stre = datetime.strftime(datetime.now().date(), '%d/%m/%Y') + " " + datetime.strftime(datetime.now(),
                                                                                              '%H:%M:%S')
        bytess = hashlib.md5(bytes(stre.encode('UTF-8')))
        s = bytess.hexdigest()
        return s

    def aesencrypt(self):
        key = bytes(self.key, 'ascii')
        iv = '\x00' * 16
        salt = self.getsalt()
        saltedpass = self.password + salt
        padedsalt = saltedpass
        bytesaltedpass = bytes(padedsalt, 'ascii')

        aes = AES.new(key, AES.MODE_CBC, iv)
        aes.block_size = 128
        encoder = PKCS7Encoder()
        encd = aes.encrypt(encoder.encode(bytesaltedpass.decode('utf-8')))
        encd64 = base64.b64encode(encd)
        return encd64.decode('utf-8')

    def aesdecrypt(self, encd):
        key = self.key
        iv = '\x00' * 16
        aes = AES.new(key, AES.MODE_CBC, iv)
        encd = base64.b64decode(encd)
        decd = aes.decrypt(encd)
        return decd.decode('utf-8')

    def run():
        print('ascii_snek')

    if __name__ == '__run__':
        run()
