import struct
import os

file_name = r'./nrf52840_xxaa.hex'
file_hex = open(file_name,'rb+')
file_length = os.path.getsize(file_name)
print("file_length=%d"%file_length)
file_hex.seek(0,2)
dst_num = 0
i=1
dst_pos = 0
need_fill_count = 0

while(dst_num <3): 
    file_hex.seek(-i,2)
    data = file_hex.read(1);
    if(data == b':'):
        dst_num += 1
    i += 1

dst_pos = i

print("i=%d,dst_pos=%d"%(i,dst_pos))

file_hex.seek(0,1)
data = file_hex.read(2);

line_data_num = int(data.decode(),16)
if(line_data_num != 0x10):
    print("need to fill")
    need_fill_count = 16 - line_data_num
    print("need_fill_count=%d"%need_fill_count)
    file_hex.seek(0,0)
    byte_data = file_hex.read(file_length)
    b_array = bytearray(byte_data)
    
    b_array[file_length-dst_pos+2] = 0x31
    b_array[file_length-dst_pos+3] = 0x30
   
    off_set = line_data_num*2 + 6
    for j in range(0,need_fill_count*2):
        b_array.insert(file_length-dst_pos+4+off_set+j,0x46)
    #print(b_array)
    f = open(r'./2.hex','wb+')
    f.write(b_array)
    f.close()
else:
    print("need not fill data")
   

file_hex.close()
