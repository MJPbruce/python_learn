
import os
import sys
from struct import *
import struct
#hex to bin
def hex_bin(hexfile,binfile):    
    fin = open(hexfile)
    fout = open(binfile,'wb')
    result =''
    for hexstr in fin.readlines():
        hexstr = hexstr.strip()
        size = int(hexstr[1:3],16)
        if int(hexstr[7:9],16) != 0:
            continue    
        #end if    
        for h in range( 0, size):
            b = int(hexstr[9+h*2:9+h*2+2],16)
            result += pack('B',b)
        #end if
        fout.write(result)        
        result=''
    #end for
    fin.close()
    fout.close()

# bin to hex
def bin_hex(binfile,hexfile):
    fbin = open(binfile,'rb')
    fhex = open(hexfile,'wb')
    offset = 0x7000
    seg_addr = 2
    

    result = ':02000004'
    result += '%02X%02X' % ((seg_addr>>8) & 0xff,seg_addr & 0xff)
    checksum = 0x02 + 0x04 + (seg_addr>>8) + seg_addr & 0xff            
    checksum = -checksum
    result+='%02X' % (checksum & 0xff)
    result += '\n'
    fhex.write(str.encode(result,'utf-8'))
    while 1:
        checksum=0
        result = ':'
        bindata = fbin.read(0x10)
        if len(bindata) == 0 :
            break
        #end if
        result += '%02X' % len(bindata)
        result += '%04X' % offset
        result += '00'
        checksum = len(bindata)
        checksum += (offset & 0xff) + (offset >> 8)

        for i in range(0,len(bindata)):
            #print(type(bytes([bindata[i]])))
            byte = struct.unpack('B',bytes([bindata[i]]))
            result += '%02X' % byte
            checksum += byte[0]
        #end for    
        checksum = 0x01 + ~checksum
        checksum = checksum & 0xff
        result += '%02X\n' % checksum
        fhex.write(str.encode(result,'utf-8'))
        offset += len(bindata)
        if offset == 0x10000:
            offset = 0            
            seg_addr += 1
            result = ':02000004'
            result += '%02X%02X' % ((seg_addr>>8) & 0xff,seg_addr & 0xff)
            checksum = 0x02 + 0x04 + (seg_addr>>8) + seg_addr & 0xff            
            checksum = -checksum
            result+='%02X' % (checksum & 0xff)
            result += '\n'
            fhex.write(str.encode(result,'utf-8'))
        #end if    
        if len(bindata) < 0x10:
            break
        #end if    
    #end while    
    seg_addr = 0x00027201
    result = ':04000005'
    result += '%04X%04X' % ((seg_addr>>16) & 0xffff,seg_addr & 0xffff)
    
    checksum = 0x04 + 0x05 + ((seg_addr>>24) & 0xff) + ((seg_addr>>16) & 0xff) + ((seg_addr>>8) & 0xff) + seg_addr & 0xff            
    checksum = -checksum
    result+='%02X' % (checksum & 0xff)
    result += '\n'
    fhex.write(str.encode(result,'utf-8'))
    
    
    end_file = ':00000001FF'
    fhex.write(str.encode(end_file,'utf-8'))
    fbin.close()
    fhex.close()
#end for

    
if len(sys.argv) != 4 or (sys.argv[1] != '-h' and sys.argv[1] != '-b'):
    print('usage:')
    print('convert binary format to hexadecimal format: ')
    print(' hexbin.py -h binfile hexfile')
    print('convert hexadecimal format to binary format:')
    print(' hexbin.py -b hexfile binfile')
    exit(0)

    
if sys.argv[1] == '-h':
    print("run bin_hex")
    bin_hex(sys.argv[2],sys.argv[3])
else:
    print("run hex_bin")
    hex_bin(sys.argv[2],sys.argv[3])
"""


str1 = r'hello world'
file = open(r'./1.hex','wb')
file.write(str.encode(str1,'gb2312'))
file.close()
"""