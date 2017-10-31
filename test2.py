"""закодовує зобр. за допомогою RSA + інш.метод2"""
import numpy as np
import cv2
import math
np.seterr(over='ignore')

# img = cv2.imread('c906c7feb240696654dab85689eccff1--acrylic-paintings-art-paintings.jpg',0)
img = cv2.imread('art.jpg',0)



print("base")
base = img.copy()
height, width = base.shape[:2]
base = cv2.resize(base,(int(width/8), int(height/8)), interpolation = cv2.INTER_CUBIC)
base = base.astype(np.float64)
cv2.imshow('base',base.astype(np.uint8))
cv2.imwrite('base2.jpg',base.astype(np.uint8))
height, width = base.shape[:2]
print("розміри ",height, width)
code = np.zeros((height, width), dtype=np.float64)
decode = np.zeros((height, width), dtype=np.float64)
print(base)
with open("base2.txt","w") as w_base:
    for i in range(height):
        for j in range(width):
            w_base.write("{} ".format(base.astype(np.uint8)[i][j]))
        w_base.write("\n")


p=17
q=11
n=p*q
f=(p-1)*(q-1)    #1080
e=103

d=87

a = ((q+p)**e)%n

print("code")
for i in range(0,height,2):
    line_x = iter(base[i])
    line_y = iter(base[i+1])
    # print(i)
    for j in range(width):
        x = next(line_x)
        y = next(line_y)
        code[i][j] = a*x + (i+1)**2         #x`
        code[i+1][j] = a*y + (i+2)**3         #y`

print(code)
cv2.imshow('code',code.astype(np.uint8))
cv2.imwrite('code2.jpg',code.astype(np.uint8))
with open("code2.txt","w") as w_code:
    for i in range(height):
        for j in range(width):
            w_code.write("{} ".format(code.astype(np.uint8)[i][j]))
        w_code.write("\n")


print("transfer")

min_val = min([min(i) for i in code])
max_val = max([max(i) for i in code])
transfer = np.zeros((height, width), dtype=np.float64)
for i in range(height):
    for j in range(width):
        transfer[i][j] = (256*(code[i][j]-min_val))/(max_val-min_val)
print("max ",max_val)
print("min ",min_val)
print("delta ",(max_val-min_val)/256)
print(transfer)

cv2.imshow('transfer',transfer.astype(np.uint8))
cv2.imwrite('transfer2.jpg',transfer.astype(np.uint8))
with open("transfer2.txt","w") as w_transfer:
    for i in range(height):
        for j in range(width):
            w_transfer.write("{} ".format(transfer.astype(np.uint8)[i][j]))
        w_transfer.write("\n")



print("back transfer")

back_transfer = np.zeros((height, width), dtype=np.float64)
for i in range(height):
    for j in range(width):
        back_transfer[i][j] = (transfer[i][j]*(max_val-min_val))/256 + min_val
print(back_transfer)

cv2.imshow('back transfer',back_transfer.astype(np.uint8))
cv2.imwrite('back_transfer2.jpg',back_transfer.astype(np.uint8))
with open("back_transfer2.txt","w") as w_back_transfer:
    for i in range(height):
        for j in range(width):
            w_back_transfer.write("{} ".format(back_transfer.astype(np.uint8)[i][j]))
        w_back_transfer.write("\n")




print("decode")

for i in range(0,height,2):
    line_x = iter(code[i])
    line_y = iter(code[i+1])
    # print(i)
    for j in range(width):
        x = next(line_x)
        y = next(line_y)
        delta_x = a*(x-(i+1)**2)
        delta_y = a*(y-(i+2)**3)
        decode[i][j] = delta_x/(a**2)        #x`
        decode[i+1][j] = delta_y/(a**2)        #x`
        

print(decode)
cv2.imshow('decode',decode.astype(np.uint8))
cv2.imwrite('decode2.jpg',decode.astype(np.uint8))
with open("decode2.txt","w") as w_decode:
    for i in range(height):
        for j in range(width):
            w_decode.write("{} ".format(decode.astype(np.uint8)[i][j]))
        w_decode.write("\n")


print("decode with back transfer")
decode_back_transfer = np.zeros((height, width), dtype=np.float64)

for i in range(0,height,2):
    line_x = iter(back_transfer[i])
    line_y = iter(back_transfer[i+1])
    # print(i)
    for j in range(width):
        x = next(line_x)
        y = next(line_y)
        delta_x = a*(x-(i+1)**2)
        delta_y = a*(y-(i+2)**3)
        decode_back_transfer[i][j] = delta_x/(a**2)        #x`
        decode_back_transfer[i+1][j] = delta_y/(a**2) 
        

print(decode_back_transfer)
cv2.imshow('back_decode',decode_back_transfer.astype(np.uint8))
cv2.imwrite('decode_back_transfer2.jpg',decode_back_transfer.astype(np.uint8))
with open("decode_back_transfer2.txt","w") as w_decode_back_transfer:
    for i in range(height):
        for j in range(width):
            w_decode_back_transfer.write("{} ".format(decode_back_transfer.astype(np.uint8)[i][j]))
        w_decode_back_transfer.write("\n")



print("delta transfer")

delta_back_decode = np.zeros((height, width), dtype=np.float64)
delta_decode = np.zeros((height, width), dtype=np.float64)
for i in range(height):
    for j in range(width):
        delta_back_decode[i][j] = math.fabs(decode_back_transfer[i][j] - base[i][j])
        delta_decode[i][j] = math.fabs(decode[i][j] - base[i][j])

delta_module_back_decode = max(max(i) for i in delta_back_decode)
delta_module_decode = max(max(i) for i in delta_decode)

print(delta_back_decode)
print(delta_decode)

print("delta_module_back_decode ",delta_module_back_decode)
print("delta_module_decode ",delta_module_decode)

# print(max(*code))
# cv2.destroyAllWindows()

k = cv2.waitKey(0)
if k == 27:         # wait for ESC key to exit
    cv2.destroyAllWindows()

    
# elif k == ord('s'): # wait for 's' key to save and exit
    # cv2.imwrite('messigray.png',img)
    # cv2.destroyAllWindows()