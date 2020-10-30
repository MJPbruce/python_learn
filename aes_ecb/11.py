
def decTohexStr(argv):  
  result = ''  
  hLen = len(argv)  
  for i in range(hLen): 
    if(argv[i] <= 15):
      result +=  '0%x'%argv[i]
    else:
      result +=  '%x'%argv[i]
      
  return result



file = open(r'.\115F-1288-0000000C-OTA_lumi.lunar.acn01.ota','rb+')
file.seek(52,0)
data = file.read(1)
print(type(data))

str = '76'

print(int(str))
"""
print(data)
cur_data = ord(data)

cur_data += 4
print(bytes([cur_data]))

file.seek(-1,1)
file.write(bytes([cur_data]))


print(ord(data))
ota_data_str = decTohexStr(data)
print(ota_data_str)
"""
file.close()