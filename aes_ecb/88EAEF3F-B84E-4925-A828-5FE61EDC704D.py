#!/usr/bin/python3
#-*- coding:utf-8 -*-
# Author: LiuChuansen
# Date  : 20201022


import sys
import os
import hashlib

from Crypto.Cipher import AES
#
# mac, installcode, xiaomikey, lumikey, did, crc
# 04CF8CDF3C737663	562065087787004E905F8E67EE2BA1EC	366D35564572364D767175366B4E5162	1741A01F88E67D5AE863109BE86F3988	000000000F32B351        6DC1

def stringToHex(s):
    bs = bytes(s, 'utf-8')
    out = ''
    for v in bs:
        out += '{:X}'.format(v)
    return out

def revertByteString(s):
    if ((len(s) % 2) != 0):
        return s
    blen = int(len(s) / 2)
    a = ""
    while blen >= 0:
        b = blen * 2
        e = blen * 2 + 2
        #print(s[b:e])
        a = a + s[b:e]
        blen = blen - 1
    return a

## 生成产测接口使用的命令字节
def toProductionCode(mac, installCode, xiaomiKey, lumiKey, deviceId, crc):
    lead = 'FE' 
    prefix = '448A'
    content = prefix + mac + installCode + xiaomiKey + lumiKey + deviceId + crc
    ## get sum
    bs = bytearray.fromhex(content)
    ss = 0
    for v in bs:
        ss = ss + v    
    ss = ss & 0xff
    checksum = '{:02X}'.format(ss)
    
    result = lead + content + checksum
    return result


    cipher = AES.new(keys, AES.MODE_ECB)
    dec = cipher.decrypt(bs)

## 加密
def keyEncrypt(data, key):
    bsData = bytearray.fromhex(data)
    bsKey = bytearray.fromhex(key)
    cipher = AES.new(bsKey, AES.MODE_ECB)
    bsDataEncrypted = cipher.encrypt(bsData)
    out = ''
    for v in bsDataEncrypted:
        out += '{:02X}'.format(v)
    return out

def output(mac, installCode, xiaomiKey, lumiKey, deviceId, crc, key, outputFile):
    user = ''' 
MAC_ADDRESS_ELEMENTS    : {mac}
INSTALL_CODE_ELEMENTS   : {installcode}
XIAOMI_KEY_ELEMENTS     : {xiaomikey}
LUMI_KEY_ELEMENTS       : {lumikey}
DEVICE_ID_ELEMENTS      : {did}
'''
    mfg = ''' 
MFG_CUSTOM_EUI_64       : {eui64}
Install Code            : {installcode}
'''
    userFile = outputFile + '.usr'
    mfgFile = outputFile + '.mfg'

    print('==> Mac Address  :', mac)
    print('==> Install Code :', installCode)
    print('==> Xiaomi Key   :', xiaomiKey)
    print('==> Lumi Key     :', lumiKey)
    print('==> Did & CRC    :', deviceId + crc)    

    if len(key) == 32:
        print('==> Encrypt xiaomikey and lumikey')
        print('==> Key:', key)
        xiaomiKey = keyEncrypt(xiaomiKey, key)
        lumiKey = keyEncrypt(lumiKey, key)

        print('==> Encrption Data')
        print('==> Xiaomi Key   :', xiaomiKey)
        print('==> Lumi Key     :', lumiKey)

    f = open(userFile, 'w')
    f.write(user.format(mac=mac, installcode=installCode, xiaomikey=xiaomiKey, lumikey=lumiKey, did=deviceId+crc))
    f.close()

    f = open(mfgFile, 'w')
    f.write(mfg.format(eui64=revertByteString(mac), installcode=installCode))
    f.close()

def printUsage(appName):
    usage='''
Usage:
 {app} [--key KEY] [--file NAME] [ALL|MAC INSTALLCODE XIAOMIKEY LUMIKEY DID CRC]
    '''
    print(usage.format(app=appName))        

def main():

    # 处理命令行参数, 先解释选项
    key = ''
    filename = ''
    args = []
    appName = os.path.basename(sys.argv[0])

    i = 1
    while i < len(sys.argv):
        if sys.argv[i].startswith('--'):
            if sys.argv[i] == '--key':
                if i < len(sys.argv) - 1:
                    key = sys.argv[i + 1]
                    i = i + 2
                else :
                    printUsage(appName)
                    sys.exit(0)  
            elif sys.argv[i] == '--file':
                if i < len(sys.argv) - 1:
                    filename = sys.argv[i + 1]
                    i = i + 2
                else :
                    printUsage(appName)
                    sys.exit(0) 
            else :
                printUsage(appName)
                sys.exit(0)
        else :
            args.append(sys.argv[i]) 
            i = i + 1           

    # 获取输入的五元组信息，支持三种形式
    # 04CF8CDF3C737663	562065087787004E905F8E67EE2BA1EC	366D35564572364D767175366B4E5162	1741A01F88E67D5AE863109BE86F3988	000000000F32B351        6DC1
    # 54EF441000026CFE  D02D88E5A5BCF299B379258033CB0979  jZZD3VNj0oEy4LrK  MFDZ7iRE8bbd5ZI1  397260923  BB1E
    # 04CF8CDF3C7376652F06BE700021FD61AFDF8798205C9A554C45726F473179465566514472594C77B615E87E713F75505DC53FEDFA113A55000000000F32B353007A
    if (len(args) < 6) and (len(args) > 0):
        s = args[0]
        if (len(s) != (16 + 32 + 32 + 32 + 16 + 4)):
            printUsage(appName)
            sys.exit(0)
        mac = s[0:16]
        installCode = s[16:48]
        xiaomiKey = s[48:80]
        lumiKey = s[80:112]
        deviceId = s[112:128]
        crc = s[128:132]

    elif (len(args) >= 6):
        mac = args[0]
        installCode = args[1]
        xiaomiKey = args[2]
        lumiKey = args[3]
        deviceId = args[4]
        crc = args[5]

        # new format keys 
        if (len(xiaomiKey) == 16) and (len(lumiKey) == 16):
            dev = int(deviceId)
            deviceId = '{:0>16X}'.format(dev)
            xiaomiKey = stringToHex(xiaomiKey)
            lumiKey = stringToHex(lumiKey)            

    else :
        printUsage(appName)
        sys.exit(0)

    ## 检查五元组是否正确
    if (len(mac) != 16):
        print("*** Invalid element: MAC")
        sys.exit(0)

    if (len(installCode) != 32):
        print("*** Invalid element: INSTALL CODE")
        sys.exit(0)    

    if (len(xiaomiKey) != 32):
        print("*** Invalid element: XIAOMI KEY")
        sys.exit(0)    

    if (len(lumiKey) != 32):
        print("*** Invalid element: LUMI KEY")
        sys.exit(0)    

    if (len(deviceId) != 16):
        print("*** Invalid element: DEVICE ID")
        sys.exit(0)  

    if (len(crc) != 4):
        print("*** Invalid element: CRC")
        sys.exit(0)  

    print('==> Production Code:')
    print(toProductionCode(mac, installCode, xiaomiKey, lumiKey, deviceId, crc))

    if len(filename) > 0:
        output(mac, installCode, xiaomiKey, lumiKey, deviceId, crc, key, filename)

if __name__=="__main__":
    main() 

"""
    bs = bytes([0x43, 0x4A, 0x1D, 0xEE, 0xF2, 0xF6, 0x0D, 0xFB, 0x75, 0x78, 0xE8, 0xE1, 0x7C, 0xB1, 0xAB, 0x55])
    keys = bytes([0x66, 0x75, 0x78, 0x69, 0x61, 0x6f, 0x6d, 0x69, 0x6e, 0x67, 0x69, 0x73, 0x62, 0x65, 0x73, 0x74])
        
    cipher = AES.new(keys, AES.MODE_ECB)
    dec = cipher.decrypt(bs)
    print(bs)
    print(dec)
"""


