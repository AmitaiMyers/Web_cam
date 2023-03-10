from datetime import datetime
import cv2, time,pandas
from datetime import datetime

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

#Create the data frame for start and end of seeing an object
df = pandas.DataFrame(columns=["Start","End"])
first_frame = None
status_list = [None,None]
times = []
video = cv2.VideoCapture(0)

while True:
    check, frame = video.read()
    status = 0
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)

    if first_frame is None:
        first_frame = gray
        continue

# the frame and threshold
    delta_frame = cv2.absdiff(first_frame, gray)
    thresh_frame = cv2.threshold(delta_frame, 150, 255, cv2.THRESH_BINARY)[1]
    thresh_frame = cv2.dilate(thresh_frame, None, iterations=2)

    (cnts, _) = cv2.findContours(thresh_frame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Whenever the cam detach an object
    for contour in cnts:
        if cv2.contourArea(contour) < 10000:
            continue
        status = 1
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
    status_list.append(status)

    #Face recognition
    faces = face_cascade.detectMultiScale(frame, scaleFactor=1.05, minNeighbors=40)
    for x, y, w, h in faces:
        img = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 3)
        img = cv2.putText(frame, "Beautiful", (x + 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 100, 255), 2)
        # add a title to the face
        cv2.imshow("Capturing", img)
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow("Capturing", frame)


    #Record the time change from 0->1 or 1->0
    if status_list[-1] == 1 and status_list[-2] == 0:
        times.append(datetime.now())
    if status_list[-1] == 0 and status_list[-2] == 1:
        times.append(datetime.now())

# Windows will appear
#     cv2.imshow("Capturing", gray)
#     cv2.imshow("Delta Frame", delta_frame)
#     cv2.imshow("Threshold Frame", thresh_frame)
    cv2.imshow("Color Frame", frame)
    key = cv2.waitKey(1)

# Quite
    if key == ord('q'):
        if status == 1:
            times.append(datetime.now())
        break
    # print(status)
# print(status_list)
print(times)

# adding data to the csv
for i in range(0,len(times),2):
    df = df.append({"Start":times[i],"End":times[i+1]},ignore_index=True)
df.to_csv("Times.csv")
video.release()
cv2.destroyAllWindows

