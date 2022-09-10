import cv2
import time
import os
import rastmanual_modulo as rtm
import mediapipe as mp
import numpy as np


wCam, hCam = 640, 480

cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

folderPath = "dedos"
myList = os.listdir(folderPath)
print(myList )

overlayList = []
for imPath in myList:
    image = cv2.imread(f'{folderPath}/{imPath}')
   # print(f'{folderPath}/{imPath}')
    overlayList.append(image)

print(len(overlayList))
pTime = 0

tipIds = [4, 8, 12, 16, 20]

detector = rtm.Detector(detectionCon=0.50)

while True:

    sucess, img = cap.read()
    img = detector.EncontraMãos(img, draw=False)
    lmList = detector.EncontraPosicao(img, draw=False)
    handsType = detector.Disting(img)
    findHands = rtm.Detector(4)
    #print(lmList)
   
    if len(lmList) != 0:
        dedos = []
        handData, handsType = findHands.Disting(img)
        for hand, handType in zip(handData, handsType):
                #Polegar Esquerdo
            if handType == 'Right':
                if lmList[tipIds[0]][1] > lmList[tipIds[0]-1][1]:
                    dedos.append(0)
                else:
                    dedos.append(1)
                # Polegar direito
            elif handType == 'Left':
                if lmList[tipIds[0]][1] < lmList[tipIds[0]-1][1]:
                    dedos.append(0)
                else:
                    dedos.append(1)


        # 4 dedos
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                dedos.append(1)
            else:
                dedos.append(0)
            
            

        #print(fingers)
        totalDedos = dedos.count(1)
        print(handsType)
        #print(totalDedos)
    
        
        h, w, c = overlayList[totalDedos].shape 
        img[0:h, 0:w] = overlayList[totalDedos]

        cv2.rectangle(img, (20, 255), (170, 425), (0, 255,0), cv2.FILLED)
        cv2.putText(img, str(totalDedos), (45, 375), cv2.FONT_HERSHEY_PLAIN, 10, (255, 0, 0), 25)

    cTime = time.time()
    fps = 1/(cTime - pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (400, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

    cv2.imshow('Image', img)
    if cv2.waitKey(10) % 0xFF == ord('q'):
        break