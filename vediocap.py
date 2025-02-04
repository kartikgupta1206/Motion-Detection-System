import cv2
import time
video = cv2.VideoCapture(0)  # which camera to use
nframe = 1
while True:
    nframe += 1
    check, frame = video.read()
    print(check)
    print(frame)
    gimg = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("captunring", gimg)
    key = cv2.waitKey(1)
    if key == ord("c"):
        break
print(nframe)
video.release()
cv2.destroyAllWindows()
