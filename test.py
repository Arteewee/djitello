from djitellopy import tello
import cv2
import numpy as np
import HandTrackingModule as htm
import FaceDetectionModule as fdm
import time


me = tello.Tello()
me.connect()
me.streamon()
w, h = 320, 240
fbRange = [6200, 6800]
pid = [0.6, 0.6, 0.4]
detector = htm.handDetector(detectionCon=0.7)
tipIds = [4, 8, 12, 16, 20]
pError = 0
pTime = 0

print("***************************************")
print("*   Drone Face Tracking Application   *")
print("*        Drone will follow you        *")
print("*        by tracking your face        *")
print("*           - How to Use -            *")
print("***************************************")
print("*            Use Hand Sign            *")
print("*   To takeoff,landing,and screenshot *")
print("***************************************")
print("*            For emergency            *")
print("*            - Controls -             *")
print("*          'e' -- Takeoff             *")
print("*          'q' -- Landing             *")
print("*          's' -- Screenshot          *")
print("*          'x' -- Exit                *")
print("***************************************")
print(me.get_battery())
time.sleep(2)


def findFace(img):
    faceCascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray,scaleFactor=1.1,
                                         minNeighbors=10,
                                         minSize=(64,64),
                                         flags=cv2.CASCADE_SCALE_IMAGE)

    myFaceListC = []
    myFaceListArea = []

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
        myFaceListArea.append(area)
        myFaceListC.append([cx, cy])
    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        return img, [[0, 0], 0]

def trackFace(me, info, w, pid, pError):
    area = info[1]
    x, y = info[0]
    fb = 0

    error = x - w // 2
    speed = pid[0] * error + pid[1] * (error - pError)
    speed = int(np.clip(speed, -100, 100))

    # greenzone
    if area > fbRange[0] and area < fbRange[1]:
        fb = 0
    # redzone back
    elif area > fbRange[1] and area != 0:
        fb = -20
    # redzone move
    elif area < fbRange[0] and area != 0:
        fb = 20

    if x == 0:
        speed = 0
        error = 0

    # print(speed,fb)

    me.send_rc_control(0, fb, 0, speed)
    return error


fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter(f"djitellofacetrack/Data/video/video_{time.strftime('%d-%m-%Y_%I-%M-%S_%p')}"+'.avi', fourcc, 30.0, (w, h)) #if fast change the value of fps
time.sleep(1/30) #if still fast try to chage the value of 1/x

while True:
    #face tracking
    img = me.get_frame_read().frame
    img = cv2.resize(img, (w, h))
    out.write(img)

    #hand
    img = detector.findHands(img, draw=True)
    lmList = detector.findPosition(img, draw=True)
    if len(lmList) !=0:
        fingers=[]


        if lmList[tipIds[0]][1] > lmList[tipIds[0]- 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        for id in range(1,5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id]-2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        totalFingers = fingers.count(1)
        if totalFingers == 1:
            me.takeoff()
            me.send_rc_control(0, 0, 25, 0)
            time.sleep(2)
            print("TAKEOFF")
        elif totalFingers == 3:
            me.land()
            print("LANDING")
        elif totalFingers == 2:
            time.sleep(0.5)
            cv2.imwrite(f'djitellofacetrack/Data/Images/{time.time()}.jpg', img)
            time.sleep(0.5)
            print('screenshoot')
        print(totalFingers)

    # print(lmList[4],lmList[8])

    # x1, y1 = lmList[4][1],lmList[4][2]
    # x2, y2 = lmList[8][1], lmList[8][2]
    # cx,cy = (x1+x2)//2, (y1+y2) //2
    #
    # # cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
    # # cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
    # # cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
    # # cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
    # # try
    # p1, f1 = lmList[9][1], lmList[9][2]
    # p2, f2 = lmList[12][1], lmList[12][2]
    # px, py = (p1 + p2) // 2, (f1 + f2) // 2
    #
    # # cv2.circle(img, (p1, f1), 15, (255, 0, 255), cv2.FILLED)
    # # cv2.circle(img, (p2, f2), 15, (255, 0, 255), cv2.FILLED)
    # # cv2.line(img, (p1, f1), (p2, f2), (255, 0, 255), 3)
    # # cv2.circle(img, (px, py), 15, (255, 0, 255), cv2.FILLED)
    #
    # length = math.hypot(x2 - x1, y2 - y1)
    # # print(length)
    #
    # length1 = math.hypot(p2 - p1, f2 - f1)
    # # print(length1)
    # if length>30 and length<45:
    #     # cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
    #     # me.takeoff()
    #     # me.send_rc_control(0, 0, 25, 0)
    #     # time.sleep(2)
    #     print("TAKEOFF")
    # elif length>100:
    #     # cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
    #     me.land()
    #     print("LAND")
    # elif length1<20:
    #     # cv2.circle(img, (cx, cy), 15, (0, 255, 0), cv2.FILLED)
    #     time.sleep(0.5)
    #     cv2.imwrite(f'djitellofacetrack/Data/Images/{time.time()}.jpg', img)
    #     time.sleep(0.5)
    #     print('screenshoot')

    #FPS
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime
    cv2.putText(img,f'FPS : {int(fps)}', (20,40), cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)

    img, info = findFace(img)
    pError = trackFace(me, info, w, pid, pError)
    print("Center", info[0], "Area", info[1])
    cv2.imshow("Output", img)
    #Emergency
    pressedKey = cv2.waitKey(1) & 0xFF
    if pressedKey == ord('e'):
        me.takeoff()
        me.send_rc_control(0, 0, 30, 0)
        time.sleep(2)
        print("TAKEOFF")
    if pressedKey == ord('f'):
        cv2.imwrite(f'djitellofacetrack/Data/Images/{time.time()}.jpg', img)
        print('screenshoot')
    elif pressedKey == ord('q'):
        me.land()
        print("LAND")
    elif pressedKey == ord('x'):
        cv2.destroyAllWindows()
        print("see you later :D")
        break