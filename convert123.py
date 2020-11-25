#coding=utf-8
import xlrd
import xlwt
from datetime import date,datetime
import binascii
import string
import sys

#def_colnum = 3



#def_colnum = int(sys.argv[1])
#print(type(def_colnum))
def_rows = int(sys.argv[1])
#def_colnum = int(input("please input a num:"))

#print("input data is:",def_colnum)

#print("please press enter finish")

#ctype :  0 empty，1 string，2 number， 3 date，4 boolean，5 error

def str_to_hex(s):
    return ''.join([hex(ord(c)).replace('0x', '') for c in s])

def hex_to_str(s):
    return ''.join([chr(i) for i in [int(b, 16) for b in s.split(' ')]])

def str_to_bin(s):
    return ' '.join([bin(ord(c)).replace('0b', '') for c in s])

def bin_to_str(s):
    return ''.join([chr(i) for i in [int(b, 2) for b in s.split(' ')]])

def print_bytes_hex(data):
    lin = ['%02X' % i for i in data]
    print(" ".join(lin))
    
def convert_fun():

    wb = xlrd.open_workbook(r'.\Ntuple.xlsx')#打开文件
    #print(wb.sheet_names())
    Tuple = wb.sheet_by_index(0)
    for i in range(1,def_rows):
        #mac 
        print('MAC:')
        print(Tuple.cell(i,1).value)    
        mac_str = Tuple.cell(i,1).value
        
        #installcode
        print('installcode:')
        print(Tuple.cell(i,2).value)
        installcode_str = Tuple.cell(i,2).value


        #mi_key
        mi_key = Tuple.cell(i,3).value
        #print(Tuple.cell(i,3).value)
        mi_key_str=str_to_hex(mi_key)
        print('mi key:')
        print(mi_key_str)

        #aqara key
        #print(Tuple.cell(def_colnum,4).value)
        aqara_key = Tuple.cell(i,4).value
        aqara_key_str=str_to_hex(aqara_key)
        print('aqara key:')
        print(aqara_key_str)


        #did 
        #print(Tuple.cell(i,5).ctype)
        #print(Tuple.cell(i,5).value)
        print('did val:')
        did=Tuple.cell(i,5).value
        str_did=hex(int(did))
        str_did_1 = str_did[2:]
        did_str = str_did_1.zfill(16)
        print(did_str)



        #crc
        print('CRC val:')
        print(Tuple.cell(i,6).value)

        crc_str = Tuple.cell(i,6).value

        sum_str = mac_str + installcode_str + mi_key_str + aqara_key_str + did_str + crc_str
        print('5 elements:')
        print(sum_str)


        file_name = str(i) + '.txt'
        print(file_name)

        file = open(file_name,'w')
        file.write(sum_str)
        file.close()



if __name__ == '__main__':
    convert_fun()


#workbook = xlwt.Workbook()



#print(int(did,10))  #can convert str_num to int num


#date_value = xlrd.xldate_as_tuple(Tuple.cell_value(1,2),wb.datemode)
#print(date_value)
#print(date(*date_value[:3]))
#print(date(*date_value[:3]).strftime('%Y/%m/%d'))