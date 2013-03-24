from Crypto.Cipher import AES 
import httplib
import urllib
import json
import json_ascii
import getpass
import base64
import hmac
import hashlib
import os

def unlock(site,enc_password=""):
    if enc_password == "":
        print '{}: Enter your API key file encryption password.'.format(site)
        enc_password = getpass.getpass()#raw_input()
    try:	
        partialpath=os.path.join('../keys/' + site)
        f = open(os.path.join(partialpath + '_salt.txt'),'r')
        salt = f.read()
        f.close()
        hash_pass = hashlib.sha512(enc_password.encode("utf-8") + salt).digest()     #create the AES container    
        crypt_key = hash_pass[:32]
        crypt_ini = hash_pass[-16:]
        f = open(os.path.join(partialpath + '_key.txt'),'r')
        ciphertext = f.read()
        f.close()
        decryptor = AES.new(crypt_key, AES.MODE_OFB, crypt_ini)
        plaintext = decryptor.decrypt(ciphertext)
        d = json.loads(plaintext)
        key = d['key']
        secret = d['secret']
    except:
        print "\n\n\nError: you may have entered an invalid password or the encrypted api key file doesn't exist"
        print "If you haven't yet generated the encrypted key file, run the encrypt_api_key.py script."
        while 1:
            pass 
    return (key,secret,enc_password)