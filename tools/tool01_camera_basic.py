import cv2
攝影機 = cv2.VideoCapture(0)
while True:
    成功擷取,畫面 = 攝影機.read()
    if not 成功擷取:
        break
    cv2.imshow("畫面:",畫面)
    if cv2.waitKey(1) ==27: #按ESC離開
        break
攝影機.release()
cv2.destroyAllWindows()
