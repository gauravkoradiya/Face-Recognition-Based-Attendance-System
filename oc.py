# -*- coding: utf-8 -*-
"""
Created on Tue Jun 26 14:09:46 2018

@author: GK
"""

#import OpenCV library
import cv2
#import matplotlib library
import matplotlib.pyplot as plt
#importing time library for speed comparisons of both classifiers
import time 
import numpy as np

def convertToRGB(img): 
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#load test iamge
gray_img = cv2.imread('image.jpg',0)
#convert the test image to gray image as opencv face detector expects gray images 
#gray_img = cv2.cvtColor(test1,cv2.COLOR_BGR2GRAY)
#if you have matplotlib installed then  
cv2.imshow('Test Image',gray_img) 
cv2.waitKey(0) 
cv2.destroyAllWindows()


#load cascade classifier training file for haarcascade 
haar_face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#let's detect multiscale (some images may be closer to camera than others) images 
faces = haar_face_cascade.detectMultiScale(gray_img, scaleFactor=1.1, minNeighbors=5);  

#print the number of faces found 
print('Faces found: ', len(faces))



#go over list of faces and draw them as rectangles on original colored
for (x, y, w, h) in faces:  
    cv2.rectangle(gray_img, (x, y), (x+w, y+h), (0,255, 0), 2)
#convert image to RGB and show image 

cv2.imshow('Test Image',gray_img )
cv2.waitKey(0) 
cv2.destroyAllWindows()





def detect_faces(f_cascade, colored_img, scaleFactor = 1.1):
 #just making a copy of image passed, so that passed image is not changed 
 img_copy = colored_img.copy()          
 
 #convert the test image to gray image as opencv face detector expects gray images
 #gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)          
 
 #let's detect multiscale (some images may be closer to camera than others) images
 faces = f_cascade.detectMultiScale(img_copy, scaleFactor=scaleFactor, minNeighbors=2);          
 
 #go over list of faces and draw them as rectangles on original colored img
 for (x, y, w, h) in faces:
      cv2.rectangle(img_copy, (x, y), (x+w, y+h), (0, 255, 0), 2)              
 
 return img_copy

#load another image 
gray_img = cv2.imread('image.jpg',0)

#call our function to detect faces 

t1 = time.time()  
faces_detected_img = detect_faces(haar_face_cascade, gray_img)  
#note time after detection 
t2 = time.time() 
#calculate time difference 
dt1 = t2 - t1 
 
#convert image to RGB and show image 
#plt.imshow(convertToRGB(faces_detected_img))
#plt.imshow(convertToRGB(faces_detected_img))
cv2.imshow('Test Image',faces_detected_img )
cv2.waitKey(0) 
cv2.destroyAllWindows()
print(dt1)
 
