import cv2
import mediapipe as mp
import time


class handDetector():
    def __init__(self, mode=False, maxHands=1, detectionCon=0.7, trackCon=0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands,
                                        self.detectionCon, self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)
        # print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms,
                                               self.mpHands.HAND_CONNECTIONS)
        return img

    def findPosition(self, img, handNo=0, draw=True):

        lmList = []
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                # print(id, lm)
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                # print(id, cx, cy)
                lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        return lmList
#hand tracking with volume gesture
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


#
# def main():
#     pTime = 0
#     cTime = 0
#     cap = cv2.VideoCapture(0)
#     detector = handDetector()
#     while True:
#         success, img = cap.read()
#         img = detector.findHands(img)
#         lmList = detector.findPosition(img)
#         if len(lmList) != 0:
#             print(lmList[4])
#
#         cTime = time.time()
#         fps = 1 / (cTime - pTime)
#         pTime = cTime
#
#         cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
#                     (255, 0, 255), 3)
#
#         cv2.imshow("Image", img)
#         cv2.waitKey(1)
#
#
# if __name__ == "__main__":
#     main()