from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64


# 加密函数
def encrypt(data: str, key: str):
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv=b'1234567890123456')  # 初始化向量（16字节）
    encrypted = cipher.encrypt(pad(data.encode(), AES.block_size))
    return base64.b64encode(encrypted).decode()


# 解密函数
def decrypt(data: str, key: str):
    cipher = AES.new(key.encode('utf-8'), AES.MODE_CBC, iv=b'1234567890123456')
    decrypted = unpad(cipher.decrypt(base64.b64decode(data)), AES.block_size)
    return decrypted.decode()
