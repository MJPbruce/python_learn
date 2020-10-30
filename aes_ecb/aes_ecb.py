"""
ECB没有偏移量
"""
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import os

"""
def add_to_16(text):
    if len(text) % 16:
        add = 16 - (len(text) % 16)
    else:
        add = 0
    text = text + ('\0' * add)
    return text


"""




def sendDataToSerialPort(sp,data):
    # data.append(fcsCheck(data,1))

    binaryData = struct.pack('B'*len(data),*data)
    wrt = sp.write( binaryData)
    # data.pop()
    logger.debug(">>>>>>>>>>>>>>>>>>>>>>>>>>>>{}", decTohexStr(data))


def decTohexStr(argv):  
  result = ''  
  hLen = len(argv)  
  for i in range(hLen): 
    if(argv[i] <= 15):
      result +=  '0%x'%argv[i]
    else:
      result +=  '%x'%argv[i]
      
  return result

def add_to_16(text):
    if len(text.encode('utf-8')) % 16:
        add = 16 - (len(text.encode('utf-8')) % 16)
    else:
        add = 0
    text = text + ('\0' * add)
    return text.encode('utf-8')

# 加密函数
def encrypt(text):
    key = 'B44aPxVIzLeP0DCa'.encode('utf-8')
    mode = AES.MODE_ECB
    text = add_to_16(text)
    print(text)
    print(len(text))
    cryptos = AES.new(key, mode)

    cipher_text = cryptos.encrypt(text)

    print(type(cipher_text))
    print(len(cipher_text))
    #return b2a_hex(cipher_text)
    
    return cipher_text
    
## 加密
## data :string  key :string
def dataEncrypt(data, key):
    bsData = bytearray.fromhex(data)
    #bsKey = bytearray.fromhex(key)
    cipher = AES.new(key, AES.MODE_ECB)
    bsDataEncrypted = cipher.encrypt(bsData)
    out = ''
    for v in bsDataEncrypted:
        out += '{:02X}'.format(v)
    return out    

## 解密
## data :string  key :string
def dataDecrypt(data, key):
    bsData = bytearray.fromhex(data)
    #bsKey = bytearray.fromhex(key)
    cipher = AES.new(key, AES.MODE_ECB)
    bsDataDecrypted = cipher.decrypt(bsData)
    out = ''
    for v in bsDataDecrypted:
        out += '{:02X}'.format(v)
    return out    



# 解密后，去掉补足的空格用strip() 去掉
def decrypt(text):
    key = 'B44aPxVIzLeP0DCa'.encode('utf-8')
    mode = AES.MODE_ECB
    cryptor = AES.new(key, mode)
    plain_text = cryptor.decrypt(a2b_hex(text))
    return bytes.decode(plain_text).rstrip('\0')



  
  
def readBinFile():
    file_name = r'D:\python_practice\aes_ecb\nrf52840_xxaa.bin'
    file = open(file_name,'rb')
    file_length = os.path.getsize(file_name)
    print(file_length)
    
    


    #file.seek(0,2)
    #length = file.tell()
    #file_length = 160
    for i in range(0,file_length,16):
        file.seek(i,0)
        file_bin_data = file.read(16)
        if(len(file_bin_data) != 16):
            print(len(file_bin_data))
        print(decTohexStr(file_bin_data))
        print(file_bin_data)
        #i += 16
    file.close()

if __name__ == '__main__':
    key = 'B44aPxVIzLeP0DCa'.encode('utf-8')
   # readBinFile()
    file_name = r'D:\python_practice\aes_ecb\nrf52840_xxaa.bin'
    file = open(file_name,'rb')
    file.seek(0,0)
    file_bin_data = file.read(16)
    #print(file_bin_data.decode(encoding="utf-8",errors="ignore"))
    #print(len(file_bin_data.decode(encoding="utf-8",errors="ignore")))
    print(type(file_bin_data))
    print("after convert data and data type:")
    print(decTohexStr(file_bin_data))
    print(type(decTohexStr(file_bin_data)))
    
    print(type(key))
    e = dataEncrypt(decTohexStr(file_bin_data), key)
    
   # e = encrypt('508402206174020099bf0200c1bd0212')  # 加密
    print(len(e))
    #d = decrypt(e)  # 解密
    
    d = dataDecrypt(e,key)
    print("encrypt:", e)
    print("decrypt:", d)
    
    
