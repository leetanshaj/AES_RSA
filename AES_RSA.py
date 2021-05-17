import hashlib
import base64
import binascii
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as Cipher_PKCS1_v1_5
from base64 import b64decode,b64encode
import random


data = 'P9k2u2OuTyBJKAtYD4Qb79MCjA5OTT9+tgPTweoSkAIa1iHZ26VRaDVHG0EZ6FtO56hyd6mTh7rZ3UAr0oGoka/Y3jWBjoiabvX8YiIL/5Np4CtQyVW46M6kwu5YFxbqDI5UPIwMZ5UTKqck6fZBByhw7VWEWJv/qR0xAx7Z68Jcs99pUp5dSr/CKe+Vv76D'
key = 'eHeluJOOO7ffoarT0MCEbXEdaOoo7Ux+juM94dRo2+Y='
iv = '6G7WY9hKgFEa7YiKJOuT0A=='
def AES_IV_DECRYPT(data, key, iv):
	unpad = lambda s : s[:-s[-1]]
	data,key,iv = list(map(base64.b64decode,[data,key,iv]))
	cipher = AES.new(key, AES.MODE_CBC, iv)
	decrypted = cipher.decrypt(data)
	clean = unpad(decrypted).decode('ascii').rstrip()
	return clean

print(AES_IV_DECRYPT(data,key,iv))

data = '{"email":"email@gmail.com","password":"Password@123","deviceID":"6c5e3cr65d94c159","hash":"xP3QjKNkIUH"}'
rkey = "".join([str(random.randint(1,9)) for i in range(10)])
fkey = hashlib.sha256(rkey.encode()).hexdigest()
key = base64.b64encode(hashlib.sha256(fkey.encode()).hexdigest().encode())
iv = "Q8epkpyJpfyF04Vd7VC82Q=="

def AES_IV_ENCRYPT(data, key, iv):
	key,iv = list(map(base64.b64decode,[key,iv]))
	key = key[:32]
	pad = lambda s : s+chr(16-len(s)%16)*(16-len(s)%16)
	cipher = AES.new(key, AES.MODE_CBC, iv)
	encrypted_64 = base64.b64encode(cipher.encrypt(pad(data))).decode('ascii')
	key, iv =list(map(base64.b64encode,[key,iv]))
	return [encrypted_64,key,iv]


def rsaEncrypt(msg):
	pubkey = 'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAuOq4r6x+pXij1R0Ou2es+DoV0ndcBoKaTL+IGFj0Z8ZzpENaqMvbfQTyBHf6oH6Pk8WSmLq9GTqXjGb8lg3JoBzeyuMqRVTJhEEeYtSJg4azpVpW57P9D6V2TPow59szNGMKdUddyr9d2yzIenKs7gARaayUBtJp6JHRpMUVC4dlSUVECj54/ZT3wkeAKaPeheV2+08GM9vWGmUhcL9ID6QDANqdvt08A+d50fwfBlAtJbqaNnUUUgP/ZMIGFvXaqgYMaM5UN1d5Rm61YzRKMAnYjIqufQebeazLZTYU1vAhi4mcTO0f2/K/M0TnFw/NSrKEdaLfWOTyQDKONpkAQQIDAQAB'
	keyDER = b64decode(pubkey)
	keyPub = RSA.importKey(keyDER)
	cipher = Cipher_PKCS1_v1_5.new(keyPub)
	cipher_text = cipher.encrypt(msg)
	emsg = b64encode(cipher_text)
	return emsg

d,key,iv = AES_IV_ENCRYPT(data,key,iv)
a = rsaEncrypt(key)
b = rsaEncrypt(iv)
data = {"a":a.decode(),"b":b.decode(),"data":data}
