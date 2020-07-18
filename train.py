import tkinter as tk
import cv2,os
import numpy as np
from PIL import Image
import pandas as pd
import datetime
import time

window = tk.Tk()

window.title("Vision ToolBox")
 
window.geometry('320x140')
 
lbl = tk.Label(window, text="Enter ID",width=10) 
lbl.place(x=3,y=5)

txt = tk.Entry(window,width=20)
txt.place(x=80, y=5)

message = tk.Label(window, text="") 
message.place(x=3, y=35)
 
def clear():
    txt.delete(0, 'end')    
    res = ""
    message.configure(text=res)
def clock():
    t=time.asctime(time.localtime(time.time()))
    if t!='':
        Time.config(text=t,font=('times 25','15'))
    window.after(100,clock)   
def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
 
    return False
 
def TakeImages():        
    Id=txt.get()
    if(is_number(Id)):
        cam = cv2.VideoCapture(0)
        harcascadePath=r"E:\tensorflow\deep-learning\haarcascade_frontalface_default.xml"
        detector=cv2.CascadeClassifier(harcascadePath)
        sampleNum=0
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)        
                #incrementing sample number 
                sampleNum=sampleNum+1
                #saving the captured face in the dataset folder
                cv2.imwrite(r"E:\tensorflow\deep-learning\TrainingImage\Train.User."+Id+"."+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                #display the frame
                cv2.imshow('frame',img)
            #wait for 100 miliseconds 
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            # break if the sample number is morethan 100
            elif sampleNum>100:
                break
        cam.release()
        cv2.destroyAllWindows() 
        res = "Images Saved for " + Id
        message.configure(text= res)
    else:
        res = "Enter Numeric Id"
        message.configure(text= res)
    
def TrainImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()#$cv2.createLBPHFaceRecognizer()
    harcascadePath =r'E:\tensorflow\deep-learning\haarcascade_frontalface_default.xml'
    detector=cv2.CascadeClassifier(harcascadePath)
    TrainingImagePath=r"E:\tensorflow\deep-learning\TrainingImage"
    faces,Ids = getImagesAndLabels(TrainingImagePath)
    recognizer.train(faces, np.array(Ids))
    recognizer.write(r"E:\tensorflow\deep-learning\TrainingImageLabel\Trainner.yml")
    res = "Image Trained" 
    message.configure(text= res)

def getImagesAndLabels(path):
    #get the path of all the files in the folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)] 
    #print(imagePaths)
    
    #create empth face list
    faces=[]
    #create empty ID list
    Ids=[]
    #now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        pilImage=Image.open(imagePath).convert('L')
        #Now we are converting the PIL image into numpy array
        imageNp=np.array(pilImage,'uint8')
        #getting the Id from the image
        Id=int(os.path.split(imagePath)[-1].split(".")[2])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)        
    return faces,Ids

def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()#cv2.createLBPHFaceRecognizer()
    recognizer.read(r"E:\tensorflow\deep-learning\TrainingImageLabel\Trainner.yml")
    harcascadePath = r"E:\tensorflow\deep-learning\haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);    
    df=pd.read_csv(r"E:\tensorflow\deep-learning\StudentDetails\StudentDetails.csv")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX        
    col_names =  ['ID','Date','Time']
    attendance = pd.DataFrame(columns = col_names)    
    while True:
        ret,im =cam.read()
        gray=cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
        faces=faceCascade.detectMultiScale(gray,1.1,10)    
        for(x,y,w,h) in faces:
            cv2.rectangle(im,(x,y),(x+w,y+h),(225,0,0),2)
            Id, conf = recognizer.predict(gray[y:y+h,x:x+w])                                   
            if(conf < 50):
                ts = time.time()      
                date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                attendance.loc[len(attendance)] = [Id,date,timeStamp]
                aa=df.loc[df['ID'] == Id]['Name'].values
                tt=str(Id)+"-"+aa
            else:
                Id='Unknown'                
                tt=str(Id)  
            if(conf > 75):
                noOfFile=len(os.listdir(r"E:\tensorflow\deep-learning\ImagesUnknown"))+1
                cv2.imwrite(r"E:\tensorflow\deep-learning\ImagesUnknown\Image"+str(noOfFile) + ".jpg", im[y:y+h,x:x+w])            
            cv2.putText(im,str(tt),(x,y+h), font, 1,(255,255,255),2)        
        attendance=attendance.drop_duplicates(keep='first',subset=['ID'])    
        cv2.imshow('im',im) 
        if (cv2.waitKey(1)==ord('q')):
            break
    ts = time.time()      
    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
    Hour,Minute,Second=timeStamp.split(":")
    fileName=r"E:\tensorflow\deep-learning\Attendance\Attendance_"+date+"_"+Hour+"-"+Minute+"-"+Second+".csv"
    attendance.to_csv(fileName,index=False)
    cam.release()
    cv2.destroyAllWindows()
    print(attendance)
  
clearButton = tk.Button(window, text="Clear", command=clear)
clearButton.place(x=210, y=0)    
takeImg = tk.Button(window, text="Take Images", command=TakeImages)
takeImg.place(x=3, y=60)
trainImg = tk.Button(window, text="Train Images", command=TrainImages)
trainImg.place(x=83, y=60)
trackImg = tk.Button(window, text="Track Images", command=TrackImages)
trackImg.place(x=166, y=60)
quitWindow = tk.Button(window, text="Quit", command=window.destroy)
quitWindow.place(x=253, y=60)
copyWrite = tk.Text(window, background=window.cget("background"), borderwidth=0,)
copyWrite.tag_configure("superscript", offset=4)
copyWrite.configure(state="disabled")
copyWrite.pack(side="top")
copyWrite.place(x=75, y=100)
Time=tk.Label(window)
Time.pack(side = "bottom")
clock()
window.mainloop()
