import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
img = cv2.imread("D:\SmarCity\AutomaticCar\images-20220630T145919Z-001\images\\055.jpg")

#-------------------------------------------------

#percent by which the image is resized
scale_percent = 70
#calculate the 50 percent of original dimensions
width = int(img.shape[1] * scale_percent / 100)
height = int(img.shape[0] * scale_percent / 100)
# dsize
dsize = (width, height)
#-------------------------------------------------

# resize image
img = cv2.resize(img, dsize)
cv2.imshow("img_contour", img)
cv2.waitKey(0)

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
cv2.imshow("thresh", thresh)
cv2.waitKey(0)
items = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
contours = items[0] if len(items) == 2 else items[1]

img_contour = img.copy()

for i in range(len(contours)):
    area = cv2.contourArea(contours[i])
    if 100 < area < 10000:
        cv2.drawContours(img_contour, contours, i, (0, 0, 255), 2)

detected = ""
for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    ratio = h/w
    area = cv2.contourArea(c)
    base = np.ones(thresh.shape, dtype=np.uint8)
    #Adjust the ratio will allow us to recognize more cubes
    if ratio > 1 and 100 < area < 10000:
        base[y:y+h, x:x+w] = thresh[y:y+h, x:x+w]
        segment = cv2.bitwise_not(base)
        print(segment)
        custom_config = r'-l eng --oem 3 --psm 10 -c tessedit_char_whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZ" '
        c = pytesseract.image_to_string(segment, config=custom_config)
        cv2.putText(img_contour, str(c)[:1], (x + int(w / 50), y + int(h / 50)), cv2.FONT_HERSHEY_SIMPLEX, 1.5,
                    (255, 0, 0), 2)
        print(c)
        detected = detected + c
        cv2.imshow("segment", segment)
        cv2.waitKey(0)

print("detected: " + detected)

cv2.imshow("img_contour", img_contour)

cv2.waitKey(0)
cv2.destroyAllWindows()