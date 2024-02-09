# importing libraries
import csv
import tkinter as tk
from tkinter import Message, Text
import cv2
import os
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import tkinter.ttk as ttk
import tkinter.font as font
from pathlib import Path
from datetime import date
from datetime import datetime as dt


def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    faces = []
    # creating empty ID list
    Ids = []
    # now looping through all the image paths and loading the
    # Ids and the images saved in the folder
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)
    return faces, Ids
# For testing phase


def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    # Reading the trained model
    recognizer.read("C:\project\Trainer.yml")
    harcascadePath = "C:\project\haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    # getting the name from "userdetails.csv"
    df = pd.read_csv(r"C:\project\UserDetails.csv")
    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    dic = {"Id": list(), "Name": list()}
    try:
        os.mkdir("C:\project\ImagesUnknown")
    except:
        print("folder exists")
    while True:
        ret, im = cam.read()
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 50):
                aa = df.loc[df["Id"] == Id]['Name'].values
                if Id not in dic["Id"]:
                    dic["Id"].append(Id)
                    dic["Name"].append(aa)
                try:
                    tt = aa
                except:
                    print()
            else:
                Id = 'Unknown'
                tt = str(Id)
            if (conf > 75):
                # "C:\project\ImagesUnknown"
                
                noOfFile = len(os.listdir(r"C:\project\ImagesUnknown"))+1
                cv2.imwrite(r"C:\project\ImagesUnknown\Image" +
                            str(noOfFile) + ".jpg", im[y:y + h, x:x + w])
            cv2.putText(im, str(tt), (x, y + h),
                        font, 1, (255, 255, 255), 2)
        cv2.imshow('im', im)
        if (cv2.waitKey(1) == ord('q')):
            break

    cam.release()
    cv2.destroyAllWindows()
    dfatt = pd.DataFrame(dic)
    now = dt.now()
    current_time = now.strftime("%H_%M")
    path1 = "C:\project\Attendance_" + \
        str(datetime.date.today())+"_"+current_time+".csv"
    dfatt.to_csv(path1, mode='w+', index=True, header=True)


TrackImages()
