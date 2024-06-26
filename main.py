import cv2
import numpy as np
import mediapipe as mp
from collections import deque
import time

# timer 
countdown_time = 30
start_time = time.time()

# Giving different arrays to handle colour points of different colour
bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]

blue_index = 0
green_index = 0
red_index = 0
yellow_index = 0

kernel = np.ones((5,5),np.uint8)

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
colorIndex = 0

# Set up the canvas
paintWindow = np.zeros((480,650,3)) + 255    # set rgb to 255 (white)

cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)


# mediapipe initialization
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

# set the RGB value start as blue 
red = 0
green = 0
blue = 255

# camera initialization
cap = cv2.VideoCapture(0)
ret = True
while ret:
    # frame reading 
    ret, frame = cap.read()

    # set the current time
    current_time = time.time()
    # Calculate the remaining time
    remaining_time = countdown_time - int(current_time - start_time)
    # Flip the frame vertically
    frame = cv2.flip(frame, 1)
    # Display the remaining time in the top right corner of the frame
    cv2.putText(frame, str(remaining_time), (frame.shape[1] - 50, 460), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Check if the countdown has ended
    if remaining_time <= 0:
        cv2.imwrite('paintWindow.png', paintWindow)
        cv2.destroyAllWindows()
        cap.release()
        exit() 

    x, y, c = frame.shape

    # change from BGR to RGB values
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    frame = cv2.rectangle(frame, (40,1), (140,65), (255,255,255), 2)
    frame = cv2.rectangle(frame, (160,1), (255,65), (255,0,0), 2)
    frame = cv2.rectangle(frame, (275,1), (370,65), (0,255,0), 2)
    frame = cv2.rectangle(frame, (390,1), (485,65), (0,0,255), 2)
    frame = cv2.rectangle(frame, (505,1), (600,65), (0,255,255), 2)
    cv2.putText(frame, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)

    # hand landmark
    result = hands.process(framergb)

    # post process the hand landmarks
    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                lmx = int(lm.x * 640)
                lmy = int(lm.y * 480)

                landmarks.append([lmx, lmy])


            # draw landmarks on camera frame
            mpDraw.draw_landmarks(frame, handslms, mpHands.HAND_CONNECTIONS)
        sum_x = sum(lm[0] for lm in landmarks)
        sum_y = sum(lm[1] for lm in landmarks)
        avg_x = sum_x /len(landmarks)
        avg_y = sum_y /len(landmarks)
        avg_position = (int(avg_x), int(avg_y))        
        center = avg_position
        thumb = (landmarks[4][0],landmarks[4][1])
        cv2.circle(frame, center, 3, (blue,green,red), 10)
        # when palm is closed
        if (thumb[1]-center[1]<30):
            bpoints.append(deque(maxlen=512))
            blue_index += 1
            gpoints.append(deque(maxlen=512))
            green_index += 1
            rpoints.append(deque(maxlen=512))
            red_index += 1
            ypoints.append(deque(maxlen=512))
            yellow_index += 1
        # when palm is open
        elif center[1] <= 65:
            if 40 <= center[0] <= 140: # Clear Button
                bpoints = [deque(maxlen=512)]
                gpoints = [deque(maxlen=512)]
                rpoints = [deque(maxlen=512)]
                ypoints = [deque(maxlen=512)]
            
                blue_index = 0
                green_index = 0
                red_index = 0
                yellow_index = 0
                # paint everything white except the palette boxes
                #paintWindow[67:,:,:] = 255
            # Blue palette
            elif 160 <= center[0] <= 255:
                    colorIndex = 0 
                    # set cursor RGB value (BGR)
                    red = 0
                    green = 0
                    blue = 255
            # Green palette
            elif 275 <= center[0] <= 370:
                    colorIndex = 1 
                    red = 0
                    green = 255
                    blue = 0
            # Red palette
            elif 390 <= center[0] <= 485:
                    colorIndex = 2 
                    red = 255
                    green = 0
                    blue = 0
            # Yellow palette
            elif 505 <= center[0] <= 600:
                    colorIndex = 3 
                    red = 255
                    green = 255
                    blue = 0
        else :
            if colorIndex == 0:
                bpoints[blue_index].appendleft(center)
            elif colorIndex == 1:
                gpoints[green_index].appendleft(center)
            elif colorIndex == 2:
                rpoints[red_index].appendleft(center)
            elif colorIndex == 3:
                ypoints[yellow_index].appendleft(center)
    # Append the next deques when nothing is detected to avoids messing up
    else:
        bpoints.append(deque(maxlen=512))
        blue_index += 1
        gpoints.append(deque(maxlen=512))
        green_index += 1
        rpoints.append(deque(maxlen=512))
        red_index += 1
        ypoints.append(deque(maxlen=512))
        yellow_index += 1

    # draw lines of each colour based on the points of the palette on the camera frame and canvas
    points = [bpoints, gpoints, rpoints, ypoints]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k - 1] is None or points[i][j][k] is None:
                    continue
                cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                

    cv2.imshow("Output", frame) 
    cv2.moveWindow("Output", 650, 0)
    cv2.imshow("Paint", paintWindow)

    if cv2.waitKey(1) == ord('q'):
        break

#  when q is pressed, exit 
cap.release()
cv2.destroyAllWindows()