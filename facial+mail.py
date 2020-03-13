from threading import *
from multiprocessing import Process
import smtplib
from email.message import EmailMessage
import imghdr
from picamera import PiCamera
import numpy as np
import cv2
import io
from picamera.array import PiRGBArray
import time



def facial():
    global dtct
    camera=PiCamera()
    camera.resolution=(640,480)
    first_frame=None
    rawCapture = PiRGBArray(camera, size=(640, 480))

    for frame in camera.capture_continuous(rawCapture,format="bgr",use_video_port=True):
        image=frame.array

        face_cascade=cv2.CascadeClassifier('/home/pi/faces.xml')

        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        faces=face_cascade.detectMultiScale(gray,1.1,5)

        for(x,y,w,h) in faces:
            cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
        print(str(len(faces))+"face")

        if len(faces)>=1:
            dtct=1
        else:
            dtct=0
        
        cv2.imshow("FRAME",image)
        cv2.imwrite("motion.jpeg",image)
        key=cv2.waitKey(1)
        rawCapture.truncate(0)

def sm():
    global dtct
    while True:
        if dtct is 1:
            email_id="niksagarwal13@gmail.com"
            email_pass="zgqnaekstnngbncs"
            
            msg=EmailMessage()
            msg['Subject']='MOTION DETECTED'
            msg['from']=email_id
            msg['to']='nikhilmeranaam@gmail.com'
            msg.set_content('This is the clicked photo')

            with open('motion.jpeg','rb') as f:
                file_data=f.read()
                file_type=imghdr.what(f.name)
                file_name=f.name

            msg.add_attachment(file_data,maintype='image',subtype=file_type,filename=file_name)

            with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:

                smtp.login(email_id,email_pass)
                smtp.send_message(msg)
                time.sleep(10)

dtct=None
t2=Thread(target=sm,args=())
t1=Thread(target=facial,args=())
t1.start()
t2.start()
t1.join()
t2.join()
