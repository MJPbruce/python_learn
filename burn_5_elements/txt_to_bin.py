import sys
import struct

txt_num = sys.argv[1]
txt_file_name = txt_num + ".txt"

with open(txt_file_name,'r') as f:
    filet = f.read()
    print(type(filet))
    #print(filet)
    strY = ''
    i = 0

with open(r".\1.bin",'wb') as g:
    for x in filet:
     	if x!='' and x!='\r'and x!='\n'and x!='\t':
            strY += x
            i+=1
            if(i%2==0):
                xHex = int(strY,16)
                xHex = struct.pack("B",xHex)
                #print(xHex)
                g.write(xHex)
                strY = ''
f.close()
g.close()
