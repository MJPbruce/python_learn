#coding=utf-8
import xlrd
import xlwt
from datetime import date,datetime
import binascii
import string

#def_colnum = 3

#def_colnum = input("please input a num:")
#print("input data is:",def_colnum)
def_colnum = int(input("please input a num:"))
print("input data is:",def_colnum)

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

wb = xlrd.open_workbook(r'D:\python_practice\Ntuple.xlsx')#打开文件

#print(wb.sheet_names())

Tuple = wb.sheet_by_index(0)



print(Tuple.cell(def_colnum,1).value)
print(Tuple.cell(def_colnum,2).value)


#mac  
mac_str = Tuple.cell(def_colnum,1).value
#installcode
installcode_str = Tuple.cell(def_colnum,2).value


#mi_key
mi_key = Tuple.cell(def_colnum,3).value
print(Tuple.cell(def_colnum,3).value)
mi_key_str=str_to_hex(mi_key)
print(mi_key_str)

#aqara key
print(Tuple.cell(def_colnum,4).value)
aqara_key = Tuple.cell(def_colnum,4).value
aqara_key_str=str_to_hex(aqara_key)
print(aqara_key_str)


#did 
#print(Tuple.cell(def_colnum,5).ctype)
#print(Tuple.cell(def_colnum,5).value)
print('did val:')
did=Tuple.cell(def_colnum,5).value
#int_did=string.atoi(did)
#int_did = int(did)

str_did=hex(int(did))
str_did_1 = str_did[2:]
#str_did_1_count = len(str_did_1)
#print(str_did_1_count)
#count1 = 16 - str_did_1_count
did_str = str_did_1.zfill(16)
print(did_str)



#crc
print('CRC val:')
print(Tuple.cell(def_colnum,6).value)

crc_str = Tuple.cell(def_colnum,6).value

sum_str = mac_str + installcode_str + mi_key_str + aqara_key_str + did_str + crc_str
print(sum_str)


file_name = str(def_colnum) + '.txt'
print(file_name)

file = open(file_name,'w')
file.write(sum_str)
file.close()



#workbook = xlwt.Workbook()



#print(int(did,10))  #can convert str_num to int num


#date_value = xlrd.xldate_as_tuple(Tuple.cell_value(1,2),wb.datemode)
#print(date_value)
#print(date(*date_value[:3]))
#print(date(*date_value[:3]).strftime('%Y/%m/%d'))