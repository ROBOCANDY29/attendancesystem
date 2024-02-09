# importing libraries
import csv
import tkinter as tk
from tkinter import Message, Text, messagebox
import cv2
import os
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as ttk
import tkinter.font as font
from pathlib import Path
from datetime import date
from datetime import datetime as dt
from PIL import ImageTk, Image
window = tk.Tk()
width, height = window.winfo_screenwidth(), window.winfo_screenheight()
window.geometry('%dx%d+0+0' % (width, height))
window.title("Face_Recogniser")  # name of the window
window.configure(background='white')
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)
global dialog
# image1 = Image.open(r"C:\project\bg.jpg")
# test = ImageTk.PhotoImage(image1)

# label1 = tk.Label(image=test)
# label1.image = test

# Position image
# label1.place(x=0, y=20)
# bgimg= tk.PhotoImage(Image.open("bg.jpg"))

# limg=Label(window,image=bgimg)
# limg.place(x=1000,y=20)
# limg.pack()


message = tk.Label(
    window, text="CamAttend", fg="white", width=52, bg="#618DD4",
    height=3, font=('times', 48, 'bold'), pady=25, justify="left")  # pady=100

message.place(x=0, y=0)


lbl = tk.Label(window, text="No.",
               width=70, height=2, fg="black",
               bg="white", font=('times', 30, ' bold '))
lbl.place(x=0, y=370)

txt = tk.Entry(window,
               width=20, bg="white",
               fg="green", font=('times', 15, ' bold '))
txt.place(x=975, y=405)


lbl2 = tk.Label(window, text="Name",
                width=70, fg="black", bg="white",
                height=2, font=('times', 30, ' bold '))
lbl2.place(x=0, y=470)

txt2 = tk.Entry(window, width=20,
                bg="white", fg="green",
                font=('times', 15, ' bold '))
txt2.place(x=975, y=505)


def exit_dialog():
    exit()


def retrain():
    dialog.destroy()
    df = pd.read_csv(r"C:\project\UserDetails.csv")
    print(id, type(id))
    name = df.loc[df["Id"] == id]['Name'].values[0]
    flag1 = 0
    Id = id
    txt.delete(0, END)
    txt.insert(0, id)
    txt2.delete(0, END)
    txt2.insert(0, name)
    flag1 = 1
    if flag1 != 0:
        if (is_number(Id) and name.isalpha()):
            cam = cv2.VideoCapture(0)  # starts capturing video from camera
            harcascadePath = "C:\project\haarcascade_frontalface_default.xml"
            detector = cv2.CascadeClassifier(harcascadePath)
            flag2 = 1
            sampleNum = 101

            while (True):
                if flag2 == 2:
                    break
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # (decreases by 1.3 times) and 5 specifies the
                # number of times scaling happens
                faces = detector.detectMultiScale(gray, 1.3, 5)

                # For creating a rectangle around the image
                for (x, y, w, h) in faces:
                    # Specifying the coordinates of the image as well
                    # as color and thickness of the rectangle.
                    # incrementing sample number for each image

                    cv2.rectangle(img, (x, y), (
                        x + w, y + h), (255, 0, 0), 2)
                    sampleNum = sampleNum + 1
                    # saving the captured face in the dataset folder
                    # TrainingImage as the image needs to be trained
                    # are saved in this folder

                    cv2.imwrite(
                        "C:\project\TrainingImage\TrainingImage"+name + "."+str(Id) + '.' + str(
                            sampleNum) + ".jpg", gray[y:y + h, x:x + w])
                    # display the frame that has been captured
                    # and drawn rectangle around it.
                    cv2.imshow('frame', img)
                # wait for 100 milliseconds
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                # break if the sample number is more than 60
                elif sampleNum > 200:

                    cam.release()
                    cv2.destroyAllWindows()
                    break
    messagebox.showinfo("Retrain", "Retraining process completed")


def open_dialog():
    global dialog
    dialog = tk.Toplevel(window)
    dialog.title("Dialog Box")

    dialog.geometry("300x150+100+100")

    label = tk.Label(
        dialog, text="You've already registered, do you wish to retrain?")
    label.pack(pady=10)

    exit_button = tk.Button(dialog, text="Exit", command=exit_dialog)
    exit_button.pack(side=tk.LEFT, padx=10)

    retrain_button = tk.Button(dialog, text="Retrain", command=retrain)
    retrain_button.pack(side=tk.RIGHT, padx=10)


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
    try:
        os.mkdir("C:\project\TrainingImage")
    except:
        print("Already exists")
    flag1 = 0
    Id = (txt.get())
    name = (txt2.get())
    try:
        df = pd.read_csv(r"C:\project\UserDetails.csv")
        dicti = df.to_dict()
        id1 = []
        name1 = []
        l = len(dicti['Id'])
        for i in range(0, l):
            id1.append(dicti['Id'][i])
            name1.append(dicti['Name'][i])
        flag1 = 1
        if ((name in name1) or (Id in id1)):
            flag1 = 0
            print("Already Registered!!!!")
    except FileNotFoundError:
        flag1 = 1
        print("File not found.")

    if flag1 != 0:
        if (is_number(Id) and name.isalpha()):
            cam = cv2.VideoCapture(0)  # starts capturing video from camera
            harcascadePath = "C:\project\haarcascade_frontalface_default.xml"
            detector = cv2.CascadeClassifier(harcascadePath)
            flag2 = 1
            try:
                recognizer = cv2.face.LBPHFaceRecognizer_create()
                recognizer.read("C:\project\Trainer.yml")
                flag2 = 0
            except:
                print("Training for the first time")
            sampleNum = 0

            while (True):
                if flag2 == 2:
                    break
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

                # (decreases by 1.3 times) and 5 specifies the
                # number of times scaling happens
                faces = detector.detectMultiScale(gray, 1.3, 5)

                # For creating a rectangle around the image
                for (x, y, w, h) in faces:
                    # Specifying the coordinates of the image as well
                    # as color and thickness of the rectangle.
                    # incrementing sample number for each image
                    if flag2 == 0:
                        global id
                        id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                        if (conf < 50):
                            open_dialog()
                            cam.release()
                            cv2.destroyAllWindows()
                            flag2 = 2
                            break

                    cv2.rectangle(img, (x, y), (
                        x + w, y + h), (255, 0, 0), 2)
                    sampleNum = sampleNum + 1
                    # saving the captured face in the dataset folder
                    # TrainingImage as the image needs to be trained
                    # are saved in this folder

                    cv2.imwrite(
                        "C:\project\TrainingImage\TrainingImage"+name + "."+str(Id) + '.' + str(
                            sampleNum) + ".jpg", gray[y:y + h, x:x + w])
                    # display the frame that has been captured
                    # and drawn rectangle around it.
                    cv2.imshow('frame', img)
                # wait for 100 milliseconds
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                # break if the sample number is more than 60
                elif sampleNum > 100:

                    cam.release()
                    cv2.destroyAllWindows()
                    break
            # releasing the resources

            # closing all the windows

            # Displaying message for the user
            if flag2 != 2:

                res = "Images Saved for ID : " + str(Id) + " Name : " + name
                # Creating the entry for the user in a csv file
                row = {"Id": [Id], "Name": [name]}
                df1 = pd.DataFrame(row)

                if os.path.isfile(r"C:\project\UserDetails.csv"):
                    csvfile = open(r"C:\project\UserDetails.csv", mode='r')
                    csvreader = csv.reader(csvfile)
                    for line in csvreader:
                        print(line)
                        ind = line[0]
                    csvfile.close()
                    row1 = {"index": [int(ind)+1], "Id": [Id], "Name": [name]}
                    df2 = pd.DataFrame(row1)
                    df2.to_csv(r"C:\project\UserDetails.csv",
                               mode='a', index=False, header=False)

                else:
                    df1.to_csv(r"C:\project\UserDetails.csv",
                               mode='a+', index=True, header=True)
                print(res)
        else:
            if (is_number(Id)):
                res = "Enter Alphabetical Name"
                print(res)
            if (name.isalpha()):
                res = "Enter Numeric Id"
                print(res)
    else:
        messagebox.showerror('Not Registered', 'ID/Name Already Exists')

        return 0
# Training the images saved in training image folder


def TrainImages():
    # Local Binary Pattern Histogram is an Face Recognizer
    # algorithm inside OpenCV module used for training the image dataset
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    # Specifying the path for HaarCascade file
    harcascadePath = "C:\project\haarcascade_frontalface_default.xml"
    # creating detector for faces
    detector = cv2.CascadeClassifier(harcascadePath)
    # Saving the detected faces in variables
    try:
        faces, Id = getImagesAndLabels("C:\project\TrainingImage")
    except:
        os.mkdir("C:\project\TrainingImage")
    # Saving the trained faces and their respective ID's
    # in a model named as "trainer.yml".
    recognizer.train(faces, np.array(Id))
    recognizer.save(r"C:\project\Trainer.yml")
    # Displaying the message
    res = "Image Trained"
    print(res)


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


def combined():
    returned = TakeImages()
    if returned != 0:
        TrainImages()


takeImg = tk.Button(window, text="Capture",
                    command=combined, fg="white", bg="#618DD4",
                    width=20, height=3, activebackground="green",
                    font=('times', 15, ' bold '))
takeImg.place(x=650, y=700)
quitWindow = tk.Button(window, text="Quit",
                       command=window.destroy, fg="white", bg="#618DD4",
                       width=20, height=3, activebackground="green",
                       font=('times', 15, ' bold '))
quitWindow.place(x=1030, y=700)
window.mainloop()
