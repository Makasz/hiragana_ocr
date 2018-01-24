import cv2
import os, pickle
import numpy as np


def create_db():
    data, names = [], []
    DIR = "C:/Users/Makasz/PycharmProjects/Test01"

    tmp = cv2.cvtColor(cv2.imread(DIR + "/r_2.jpg"), cv2.COLOR_BGR2GRAY)
    for foldername in os.listdir(DIR + "/letters/"):
        for filename in os.listdir(DIR + "/letters/" + foldername + "/"):
            print("Processing file " + DIR + "/letters/" + foldername + "/" + filename)
            img = cv2.imread(DIR +  "/letters/" + foldername + "/" + filename)
            bitmap = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            letter = cv2.resize(bitmap, (300, 300))
            cv2.imwrite("a.jpg", letter)
            for i in range(300):
                for j in range(300):
                    tmp[i,j] = tmp[i,j] + (letter[i,j]/255)*2
        data.append(tmp)
        tmp = cv2.cvtColor(cv2.imread(DIR + "/r_2.jpg"), cv2.COLOR_BGR2GRAY)
        names.append(foldername)
    # with open("data.txt", 'wb') as f:
    #     pickle.dump(data, f)
    with open("names.txt", 'wb') as f:
        pickle.dump(names, f)
    return data
