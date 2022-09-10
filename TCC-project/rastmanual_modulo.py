from cv2 import cvtColor
import mediapipe as mp
import cv2
import time


class Detector():
    def __init__(self, mode=False, maxHands = 2, detectionCon=0.5, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands()
        self.mpDraw = mp.solutions.drawing_utils

    def EncontraMãos(self, img, draw=True):

        imgRGB = cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results  = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return img

    def EncontraPosicao(self, img, handNo=0, draw=True):
        
        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                #print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x*w), int(lm.y*h)
                #print(id, cx, cy)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255,0,255), cv2.FILLED)

        return lmList
    def Disting(self, img):

        myHands =[]
        handsType = []
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        results=self.hands.process(imgRGB)

        if results.multi_hand_landmarks != None:
            #print(results.multi_handedness)
            for hand in results.multi_handedness:
                #print(hand)
                #print(hand.classification)
                #print(hand.classification[0])
                handType = hand.classification[0].label
                handsType.append(handType)
            for handLandMarks in results.multi_hand_landmarks:
                myHand=[]
                for landMark in handLandMarks.landmark:
                    myHand.append((int(landMark.x*width),int(landMark.y*height)))
                myHands.append(myHand)
        return myHands, handsType

width=640
height=480
findHands= Detector(4)

def main():

    pTime = 0
    cTime = 0
    cap = cv2.VideoCapture(0)
    detector = Detector()


    while True:
        success, img = cap.read()
        img = detector.EncontraMãos(img, draw=False)
        lmList = detector.EncontraPosicao(img, draw=False)
        if len(lmList) != 0:
            #print(lmList[4])
            img=cv2.resize(img,(width,height))
            handData, handsType = findHands.Disting(img)
            for hand, handType in zip(handData, handsType):
                for ind in [0,5,6,7,8]:
                    if handType == 'Right':
                        handColor = (255, 0, 0)
                    if handType == 'Left':
                        handColor = (0, 0, 255)
                    cv2.circle(img,hand[ind],15, handColor, 5)

        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255,0,255), 2)


        cv2.imshow('Image', img)
        if cv2.waitKey(10) % 0xFF == ord('q'):
           break





if __name__ == "__main__":
    main()
