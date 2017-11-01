"""закодовує"""
import numpy as np
import cv2
import math


image = cv2.imread('art.jpg',0)
height, width = image.shape[:2]
image = cv2.resize(image,(int(width/2), int(height/2)), interpolation = cv2.INTER_CUBIC)
# cv2.imshow('base',img.astype(np.uint8)

cv2.namedWindow('image')




def nothing(x):
    pass

# create trackbars for color change
cv2.createTrackbar('R','image',0,255,nothing)
cv2.createTrackbar('G','image',0,255,nothing)
cv2.createTrackbar('B','image',0,255,nothing)

# create switch for ON/OFF functionality
switch = '1 : метод №1 \n2 : метод №2'
cv2.createTrackbar(switch, 'image',0,1,nothing)

while(1):
    cv2.imshow('image',image)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    # get current positions of four trackbars
    r = cv2.getTrackbarPos('R','image')
    g = cv2.getTrackbarPos('G','image')
    b = cv2.getTrackbarPos('B','image')
    s = cv2.getTrackbarPos(switch,'image')

    # if s == 0:
    #     img[:] = 0
    # else:
    #     img[:] = [b,g,r]







# k = cv2.waitKey(0)
# if k == 27:         # wait for ESC key to exit
#     cv2.destroyAllWindows()
cv2.destroyAllWindows()

    
# elif k == ord('s'): # wait for 's' key to save and exit
    # cv2.imwrite('messigray.png',img)
    # cv2.destroyAllWindows()