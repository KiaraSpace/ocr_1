import cv2
import numpy as np
import easyocr

img = cv2.imread("demo3.jpeg")

reader = easyocr.Reader(["en"])
result = reader.readtext(img, allowlist = 'ABCDEFGHJKLMNOPQRSTTUVWXYZ')

for res in result:
    print(result)
    pt0 = res[0][0]
    pt1 = res[0][1]
    pt2 = res[0][2]
    pt3 = res[0][3]

    cv2.rectangle(img, pt0, (pt1[0], pt1[1]-23),(166,56,242),-1)
    cv2.putText(img, res[1], (pt0[0], pt0[1]-3),2,0.8,(255,255,255),1)

    cv2.circle(img, pt0, (255,0,0), 2)
    cv2.circle(img, pt1, (0,255,0), 2)
    cv2.circle(img, pt2, (0,0,255), 2)
    cv2.circle(img, pt2, (0,255,255), 2)
cv2.waitKey(0)
cv2.destroyAllWindows()