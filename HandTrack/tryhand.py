#!/usr/bin/env python
import cv2 , time
import numpy as np

def main():
    cap = cv2.VideoCapture(0)
    while(cap.isOpened()):
        img       = cap.read()

        skinMask = HSVBin(img)
        contours= getContours(skinMask , img)
        cv2.drawContours(img, contours, -1, (0, 255, 0), 2)
        cv2.imshow('capture', img)


        k = cv2.waitKey(10)
        #if k == 27:
        #    break
def getContours(img, img1):
    kernel = np.ones((5,5),np.uint8)
    closed = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)
    closed = cv2.morphologyEx(closed, cv2.MORPH_CLOSE, kernel)
    contours, h  = cv2.findContours(closed, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    validContours = [];
    for cont in contours:
        if cv2.contourArea(cont) > 9000:
            x,y,w,h = cv2.boundingRect(cont)
            if h/w > 0.75:
                validContours.append(cv2.convexHull(cont))
                rect = cv2.minAreaRect(cont)
                box = cv2.cv.BoxPoints(rect)
                validContours.append(np.int0(box))
                im = img1[y-20: y + h + 20, x -20: x + w +20]  #img[y: y + h, x: x + w]
                cv2.imshow('hand', im)
                cv2.imwrite('hand/messigray.png',im)
                


    return validContours 



def HSVBin(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    lower_skin = np.array([100, 50, 0])
    upper_skin = np.array([125, 255, 255])

    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    res = cv2.bitwise_and(img, img, mask=mask)
    return mask



if __name__ == '__main__':
    main()