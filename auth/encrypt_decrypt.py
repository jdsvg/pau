from Crypto.Cipher import AES

from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

import os
import binascii
import string
import random

class Encriptar_Datos:

    def encrypt_AES_GCM(self, password):
        x_cod_seg = ""
        llave = ""
        for i in range(5):
            x_cod_seg += random.choice(string.ascii_letters) + str(random.randint(0, 9))
        code_sec = bytes(x_cod_seg, 'utf-8')
        kdfSalt = os.urandom(16)
        secretKey = self.generate_secret_key(code_sec, kdfSalt)
        aesCipher = AES.new(secretKey, AES.MODE_GCM)
        ciphertext, authTag = aesCipher.encrypt_and_digest(password)
        encryptedMsg = [kdfSalt, aesCipher.nonce, authTag, code_sec, ciphertext]
        for indice in encryptedMsg:  # Convirtiendo datos
            llave += binascii.hexlify(indice).decode("utf-8")  # From bin to hex to str
        return llave

    def decrypt_AES_GCM(self, llave, password):
        # kdfSalt*: llave[:32]
        # aesCipher*: llave[32:64]
        # authTag*: llave[64:96]
        # code_sec*: llave[96:116]
        # ciphertext*: llave[116:]
        secretKey = self.generate_secret_key(binascii.unhexlify(((llave[96:116]).encode('utf-8'))),
                                            binascii.unhexlify(((llave[:32]).encode('utf-8'))))
        aesCipher = AES.new(secretKey, AES.MODE_GCM,
                            binascii.unhexlify(((llave[32:64]).encode('utf-8'))))
        plaintext = aesCipher.decrypt_and_verify(binascii.unhexlify(((llave[116:]).encode('utf-8'))),
                                            binascii.unhexlify(((llave[64:96]).encode('utf-8'))))
        if plaintext.decode('utf-8') == password:
            return True
        else:
            return False
        

    def generate_secret_key(self, code_sec, kdfSalt):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            salt=kdfSalt,
            iterations=100000,
            length=32
        )
        secretKey = kdf.derive(code_sec)
        return secretKey



# obj_Encriptar_Datos = Encriptar_Datos(); password = "unacontraseñamuysecreta"
# 
# ENCRIPTAR 
# encryptedMsg = obj_Encriptar_Datos.encrypt_AES_GCM(bytes(password, 'utf-8'))
# 
# DESENCRIPTAR
# decryptedMsg = obj_Encriptar_Datos.decrypt_AES_GCM(encryptedMsg, "unacontraseñamuysecreta"); print("Password: ", decryptedMsg)

