"""
ECB没有偏移量
"""
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
import os
import struct




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



  
def readBinFileAndEncrypt(file_name,key):
    file = open(file_name,'rb')
    file_length = os.path.getsize(file_name)
    print(file_length)
    bin_fill_len = 0
    while(file_length % 16):
        file_length += 1
    print(file_length)
   
    #file_length = 160
    out = ''
    for i in range(0,file_length,16):
        file.seek(i,0)
        file_bin_data = file.read(16)
        data_str = decTohexStr(file_bin_data)
        if(len(file_bin_data) != 16):
            bin_fill_len = 16 - len(file_bin_data)
            print(len(file_bin_data))
            print("bin_fill_len=%d",bin_fill_len)
            data_str += bin_fill_len * 'FF'
        out += dataEncrypt(data_str,key)
        #print(decTohexStr(file_bin_data))
        
    file.close()
    return out
    
def str_to_txt(file_name,str_data,op_mode):
    file_txt = open(file_name,op_mode)
    file_txt.write(str_data)
    file_txt.close()
    
    
def txt_to_bin(src_file_name,dst_file_name):
    bin_file = open(dst_file_name,'wb')
    txt_file = open(src_file_name,'r')
    filet = txt_file.read()
    strY = ''
    i = 0
    for x in filet:
     	if x!='' and x!='\r'and x!='\n'and x!='\t':
            strY += x
            i+=1
            if(i%2==0):
                xHex = int(strY,16)
                xHex = struct.pack("B",xHex)
                #print(xHex)
                bin_file.write(xHex)
                strY = ''
    bin_file.close()
    
    
def read_ota_file(ota_fil_name,read_size):
    file = open(ota_fil_name,'rb')
    data = file.read(read_size)
    ota_data_str = decTohexStr(data)
    print(ota_data_str)
    file.close()
    return ota_data_str


#115F-1288-0000000C-
if __name__ == '__main__':
    out = ''
    key = 'w1EHnDKllb6rmbZM'.encode('utf-8')  # key :bytes type
    file_name = r'.\nrf52840_xxaa.bin'
    ota_file_name = r'.\OTA_lumi.lunar.acn01.zigbee'
    ota_str_data = read_ota_file(ota_file_name,298)
    str_to_txt(r'.\encrypt.txt',ota_str_data,'w+')
    
    
    
    out = readBinFileAndEncrypt(file_name,key)
    #print(out)
    #print(type(out))
    #print(len(out))
    str_to_txt(r'.\encrypt.txt',out,'a+')
    txt_to_bin(r'.\encrypt.txt',r'.\encrypt.bin')
    
    
    
    ##解密操作产生文件
    d = dataDecrypt(out,key)
    #print(d)
    str_to_txt(r'.\decrypt.txt',d,'w+')
    txt_to_bin(r'.\decrypt.txt',r'.\decrypt.bin')
      
   

    #file = open(file_name,'rb')
    #file.seek(0,0)
    #file_bin_data = file.read(16)
    #
    #
    #
    #print(decTohexStr(file_bin_data))
    #
    #e = dataEncrypt(decTohexStr(file_bin_data), key)
    #d = dataDecrypt(e,key)
    #print("encrypt:", e)
    #print("decrypt:", d)
    #
    
