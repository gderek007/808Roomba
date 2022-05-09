import cv2
import numpy as np
import sys

video_in = sys.argv[1]
video_out = sys.argv[2]

cap = cv2.VideoCapture(video_in)

frame_width = int( cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height =int( cap.get( cv2.CAP_PROP_FRAME_HEIGHT))

fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
out = cv2.VideoWriter(video_out, fourcc, 5.0, (2208, 1224))

ret, frame1 = cap.read()
ret, frame2 = cap.read()
og_frame = frame1

while type(frame2) == np.ndarray:
    diff = cv2.absdiff(frame1, frame2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    _, thresh = cv2.threshold(blur, 40, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)

        for i in range(w):
            for j in range(h):
                og_frame[y + j, x + i] = [0, 0, 0]    

        if cv2.contourArea(contour) < 1000:
            continue
        
        cv2.rectangle(frame1, (x, y), (x+w, y+h), (0, 255, 0), 2)

    image2 = cv2.resize(og_frame, (2208, 1224))
    out.write(image2)

    cv2.imshow("feed", frame1)
    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(40) == 27:
        break

black_pixel_count = 0
for i in range(2208):
    for j in range(1224):
        if list(og_frame[j, i]) == [0, 0, 0]:
            black_pixel_count += 1
print("percent cleaned: ", black_pixel_count / (1224 * 2208))

cv2.destroyAllWindows()
cap.release()
out.release()