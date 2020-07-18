# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 10:29:12 2018

@author: GK
"""
#import OpenCV library
import cv2
#import matplotlib library
import matplotlib.pyplot as plt
#importing time library for speed comparisons of both classifiers
import time 
import numpy as np
def detect_faces(f_cascade, colored_img, scaleFactor = 1.1):
 #just making a copy of image passed, so that passed image is not changed 
 img_copy = colored_img.copy()          
 
 #convert the test image to gray image as opencv face detector expects gray images
 #gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)          
 
 #let's detect multiscale (some images may be closer to camera than others) images
 faces = f_cascade.detectMultiScale(img_copy, scaleFactor=scaleFactor, minNeighbors=2)       
 
 #go over list of faces and draw them as rectangles on original colored img
 for (x, y, w, h) in faces:
      cv2.rectangle(img_copy, (x, y), (x+w, y+h), (0, 255, 0), 2)              
 
 return img_copy

#load cascade classifier training file for lbpcascade 
lbp_face_cascade = cv2.CascadeClassifier('lbpcascade_frontalface.xml')  
 
#load test image 
test2 = cv2.imread('image.jpg',0) 
 
#call our function to detect faces 
t1 = time.time() 
faces_detected_img = detect_faces(lbp_face_cascade, test2)  

#note time after detection 
t2 = time.time() 
#calculate time difference 
dt1 = t2 - t1 
cv2.imshow('Test Image',faces_detected_img )
cv2.waitKey(0) 
cv2.destroyAllWindows()
print(dt1)