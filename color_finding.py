import cv2
import os
import numpy as np
import rgb_to_binary
import pickle
import sys

DIR = "C:/Users/Makasz/PycharmProjects/Test01"

print('Argument 1:', str(sys.argv[1]))

max_ar = []
arg = int(sys.argv[1])
if arg == 1:
    data = rgb_to_binary.create_db()
    with open("data.txt", 'wb') as f:
        pickle.dump(data, f)
if arg == 0:
    with open("data.txt", 'rb') as f:
        data = pickle.load(f)

with open("names.txt", 'rb') as f:
    names = pickle.load(f)
    print(names)


def recognize_letter(img2):
    score, a, max, maxa = 0, 0, 0, 0
    for img in data:
        cv2.imwrite("aaa.jpg", img*50)
        for i in range(len(img)):
            for j in range(len(img)):
                if img2[i,j] > 0:
                    score = score + img[i,j]
        if score > max:
            max = score
            maxa = a
        a = a + 1
        score = 0
        max_ar.append(max)
    print("Best score for " + str(maxa) + ": " + str(max) + "   Letter: " + names[maxa])
    return names[maxa]



a = 0
for filename in os.listdir(DIR + "/raw/"):
    a = a +1
    print("Processing file " + filename)
    img = cv2.imread(DIR + "/raw/" + filename)
    v = np.median(img)
    height = len(img)
    width = len(img[0])
    kernel = np.ones((5, 5), np.uint8)
    bitmap = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    bitmap = cv2.adaptiveThreshold(bitmap, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 151, 20)  # Mozna użyc adaptive/otsu threshold
    img_dil, img_erd = [], bitmap
    for i in range(10):
        img_dil = cv2.dilate(img_erd, kernel, iterations=1)
        img_erd = cv2.erode(img_dil, kernel, iterations=1)
    img_erd = cv2.dilate(img_dil, kernel, iterations=3)
    bitmap = img_erd
    img_cnt, cnts, hierarchy = cv2.findContours(bitmap.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    MIN_LETTER_SIZE = height * width / 200
    for i in range(len(cnts)):
        moments = cv2.moments(cnts[i])
        if cv2.contourArea(cnts[i]) < MIN_LETTER_SIZE or moments['mu02'] < 500.0:
            continue
        else:
            x, y, w, h = cv2.boundingRect(cnts[i])
            letter = bitmap[y: y + h, x: x + w]
            letter = cv2.resize(letter, (300, 300))
            nname = recognize_letter(letter)
            cv2.imwrite("final\\" + str(a) + str(i) + "_" + "_" + nname + ".jpg", letter)

