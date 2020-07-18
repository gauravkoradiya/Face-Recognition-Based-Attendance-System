# -*- coding: utf-8 -*-
"""
Created on Wed Jun 27 09:55:51 2018

@author: GK
"""

import numpy as np
import cv2

#import matplotlib library
import matplotlib.pyplot as plt
#importing time library for speed comparisons of both classifiers
import time 
import numpy as np

def convertToRGB(img): 
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
def detect_faces(f_cascade, colored_img, scaleFactor = 0.85):
    
    
 #just making a copy of image passed, so that passed image is not changed 
    img_copy = colored_img.copy()          
 
 #convert the test image to gray image as opencv face detector expects gray images
 #gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)          
 
 #let's detect multiscale (some images may be closer to camera than others) images
    faces = f_cascade.detectMultiScale(img_copy,scaleFactor=scaleFactor, minNeighbors=3);          
 
 #go over list of faces and draw them as rectangles on original colored img
    for (x, y, w, h) in faces:
        cv2.rectangle(img_copy, (x, y), (x+w, y+h), (0, 255, 0), 2)              
 
    return img_copy
    
haar_face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)
while(cap.isOpened()):  # check !
    # capture frame-by-frame
    ret, frame = cap.read()

    if ret: # check ! (some webcam's need a "warmup")
        # our operation on frame come here
        #gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_image = cv2.imread(frame,0)

        #faces_detected_img = detect_faces(haar_face_cascade, gray_image)
         #let's detect multiscale (some images may be closer to camera than others) images
        faces = haar_face_cascade.detectMultiScale(gray_image,scaleFactor=1.03, minNeighbors=3);          
 
 #go over list of faces and draw them as rectangles on original colored img
        for (x, y, w, h) in faces:
            cv2.rectangle(gray_image, (x, y), (x+w, y+h), (255, 0, 0), 2)              
 
        # Display the resulting frame
        cv2.imshow('frame',gray_image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# When everything is done release the capture
cap.release()
cv2.destroyAllWindows()

import numpy as np
import cv2

cap = cv2.VideoCapture(0)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()






import numpy as np
import cv2

cap = cv2.VideoCapture(0)

# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))

while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
        frame = cv2.flip(frame,0)

        # write the flipped frame
        out.write(frame)

        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break

# Release everything if job is finished
cap.release()
out.release()
cv2.destroyAllWindows()