
#creating module to read text from image for captcha. 

import cv2
import numpy as np

import pytesseract

# read image
def imageText():
    
    #get the image
    img = cv2.imread('captcha.jpg')

    # convert image to hsv colorspace
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)

    # threshold saturation image
    thresh1 = cv2.threshold(s, 92, 255, cv2.THRESH_BINARY)[1]

    # threshold value image and invert
    thresh2 = cv2.threshold(v, 128, 255, cv2.THRESH_BINARY)[1]
    thresh2 = 255 - thresh2

    # combine the two threshold images as a mask
    mask = cv2.add(thresh1, thresh2)

    # use mask to remove lines in background of input
    result = img.copy()
    result[mask == 0] = (255, 255, 255)


    # save output image
    cv2.imwrite('temp.png', result)

    image = cv2.imread("temp.png")
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    se = cv2.getStructuringElement(cv2.MORPH_RECT, (8, 8))
    bg = cv2.morphologyEx(image, cv2.MORPH_DILATE, se)
    out_gray = cv2.divide(image, bg, scale=255)
    out_binary = cv2.threshold(out_gray, 0, 255, cv2.THRESH_OTSU)[1]

    # cv2.imshow('binary', out_binary)
    cv2.imwrite('binary.png', out_binary)

    # cv2.imshow('gray', out_gray)
    cv2.imwrite('gray.png', out_gray)

    myconfig = r"--psm 6"
    img = cv2.imread('binary.png')
    return pytesseract.image_to_string(img).replace(" ", "")
