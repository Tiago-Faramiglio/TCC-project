import cv2
import time
import rastmanual_modulo as rtm





pTime = 0
cTime = 0
cap = cv2.VideoCapture(0)
detector = rtm.Detector()


while True:
    success, img = cap.read()
    img = detector.EncontraMãos(img)
    lmList = detector.EncontraPosicao(img)
    if len(lmList) != 0:
        print(lmList[0])

    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 2)

     
    cv2.imshow('Image', img)
    if cv2.waitKey(10) % 0xFF == ord('q'):
        break
