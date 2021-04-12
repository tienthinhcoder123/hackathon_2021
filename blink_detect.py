#All the imports go here
import numpy as np
import cv2
import time
import timeit
import datetime as date
import logging as log
import pyodbc
import random
import socket
def connect(id,):
    cnxn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                          "Server=LAPTOP-71I31G2M;"
                          "Database=StudentMonitoring;"
                          "Trusted_Connection=yes;")

    cursor = cnxn.cursor()

    cursor.execute('SELECT * FROM dbo.person ')
    for row in cursor:
        print('row = %r' % (row,))

def insertToDataBase(_id, _ip, _len_eye, _time):
    cnxn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
                          "Server=LAPTOP-71I31G2M;"
                          "Database=StudentMonitoring;"
                          "Trusted_Connection=yes;")

    cursor = cnxn.cursor()
    cursor.execute('''
                    INSERT INTO dbo.person (id, ip,len_eye,timer )
                    VALUES(_id, _ip, _len_eye, _time)
                    ''')


#Initializing the face and eye cascade classifiers from xml files
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')

#Variable store execution state
first_read = True

#Starting the video capture
cap = cv2.VideoCapture(0)
ret,img = cap.read()
log.basicConfig(filename='app.log', filemode='w',format='%(asctime)s - %(message)s', level=log.INFO)
log.info('Camera Initialized')

#variable declaration
blinktimes = 0
times = 0


while(ret):

    timeelasped = time.time()
    ret,img = cap.read()
    #Coverting the recorded image to grayscale
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #Applying filter to remove impurities
    gray = cv2.bilateralFilter(gray,5,1,1)

    #Detecting the face for region of image to be fed to eye classifier
    faces = face_cascade.detectMultiScale(gray, 1.3, 5,minSize=(200,200))
    if(len(faces)>0):
        timeelasped = time.time()
        for (x,y,w,h) in faces:
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

            #roi_face is face which is input to eye classifier
            roi_face = gray[y:y+h,x:x+w]
            roi_face_clr = img[y:y+h,x:x+w]
            eyes = eye_cascade.detectMultiScale(roi_face,1.3,5,minSize=(50,50))

            #Examining the length of eyes object for eyes
            if(len(eyes)>=2):
                #Check if program is running for detection
                if(first_read):
                    cv2.putText(img, "Eye detected press s to begin", (70,70), cv2.FONT_HERSHEY_PLAIN, 3,(0,255,0),2)
                    '''n = random.random()
                    hostname = socket.gethostname()
                    ip_address = socket.gethostbyname(hostname)
                    insertToDataBase(n, ip_address, str(len(eyes)), str(date.datetime.now()))'''
                    log.info("eyes detected " + str(len(eyes)) + " at " + str(date.datetime.now()))

                else:
                    cv2.putText(img, "Eyes open!", (70,70), cv2.FONT_HERSHEY_PLAIN, 2,(255,255,255),2)
                    log.info("eyes open " + str(len(eyes)) + " at " + str(date.datetime.now()))
            else:

                if(first_read):
                    timenoeye = time.time()
                    #To ensure if the eyes are present before starting
                    cv2.putText(img, "No eyes detected", (70,70), cv2.FONT_HERSHEY_PLAIN, 3,(0,0,255),2)
                    log.info("unindentified eyes" + " at " + str(date.datetime.now()))

                else:
                    #This will print on console and restart the algorithm
                    print("Blink detected--------------")
                    cv2.waitKey(3000)
                    first_read=True

    else:
        cv2.putText(img,"No face detected",(100,100),cv2.FONT_HERSHEY_PLAIN, 3, (0,255,0),2)
        time.sleep(.001)
        times += 1
        print(times)

    #Controlling the algorithm with keys
    cv2.imshow('img',img)
    a = cv2.waitKey(1)
    if(a==ord('q')):
        print(blinktimes)
        print(times)
        break
    elif(a==ord('s') and first_read):
        #This will start the detection
        first_read = False


cap.release()
cv2.destroyAllWindows()
