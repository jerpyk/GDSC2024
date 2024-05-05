# All the imports go here
import cv2
import numpy as np
import mediapipe as mp
from collections import deque
<<<<<<< Updated upstream:fingerpainter.py


# Giving different arrays to handle colour points of different colour
bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]


# These indexes will be used to mark the points in particular arrays of specific colour
blue_index = 0
green_index = 0
red_index = 0
yellow_index = 0

#The kernel to be used for dilation purpose 
kernel = np.ones((5,5),np.uint8)

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
colorIndex = 0
img = cv2.imread('apple.jpg')
size = 100
img = cv2.resize(img, (size,size))

gryImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ret, mask = cv2.threshold(gryImg, 1, 255, cv2.THRESH_BINARY)

# Here is code for Canvas setup
paintWindow = np.zeros((500,650,3)) + 255    #set rgb to 255 (white)
paintWindow = cv2.rectangle(paintWindow, (40,1), (140,65), (0,0,0), 2)
paintWindow = cv2.rectangle(paintWindow, (160,1), (255,65), (255,0,0), 2)
paintWindow = cv2.rectangle(paintWindow, (275,1), (370,65), (0,255,0), 2)
paintWindow = cv2.rectangle(paintWindow, (390,1), (485,65), (0,0,255), 2)
paintWindow = cv2.rectangle(paintWindow, (505,1), (600,65), (0,255,255), 2)

cv2.putText(paintWindow, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)


# initialize mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils

red = 0
green = 0
blue = 255

# Initialize the webcam
cap = cv2.VideoCapture(0)
ret = True
while ret:
    # Read each frame from the webcam
    ret, frame = cap.read()

    region = frame[-size-10:-10, -size-10:-10]
    region[np.where(mask)] = 0
    region += img
    x, y, c = frame.shape

    # Flip the frame vertically
    frame = cv2.flip(frame, 1)
    #hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    frame = cv2.rectangle(frame, (40,1), (140,65), (0,0,0), 2)
    frame = cv2.rectangle(frame, (160,1), (255,65), (255,0,0), 2)
    frame = cv2.rectangle(frame, (275,1), (370,65), (0,255,0), 2)
    frame = cv2.rectangle(frame, (390,1), (485,65), (0,0,255), 2)
    frame = cv2.rectangle(frame, (505,1), (600,65), (0,255,255), 2)
    cv2.putText(frame, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    #frame = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

    # Get hand landmark prediction
    result = hands.process(framergb)

    # post process the result
    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                # print(id, lm)
                # print(lm.x)
                # print(lm.y)
                lmx = int(lm.x * 640)
                lmy = int(lm.y * 480)

                landmarks.append([lmx, lmy])


            # Drawing landmarks on frames
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

                paintWindow[67:,:,:] = 255
            elif 160 <= center[0] <= 255:
                    colorIndex = 0 # Blue
                    # set cursor RGB value (BGR)
                    red = 0
                    green = 0
                    blue = 255
            elif 275 <= center[0] <= 370:
                    colorIndex = 1 # Green
                    red = 0
                    green = 255
                    blue = 0
            elif 390 <= center[0] <= 485:
                    colorIndex = 2 # Red
                    red = 255
                    green = 0
                    blue = 0
            elif 505 <= center[0] <= 600:
                    colorIndex = 3 # Yellow
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
    # Append the next deques when nothing is detected to avois messing up
    else:
        bpoints.append(deque(maxlen=512))
        blue_index += 1
        gpoints.append(deque(maxlen=512))
        green_index += 1
        rpoints.append(deque(maxlen=512))
        red_index += 1
        ypoints.append(deque(maxlen=512))
        yellow_index += 1

    # Draw lines of all the colors on the canvas and frame
    points = [bpoints, gpoints, rpoints, ypoints]
    # for j in range(len(points[0])):
    #         for k in range(1, len(points[0][j])):
    #             if points[0][j][k - 1] is None or points[0][j][k] is None:
    #                 continue
    #             cv2.line(paintWindow, points[0][j][k - 1], points[0][j][k], colors[0], 2)
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k - 1] is None or points[i][j][k] is None:
                    continue
                cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                if not center[1] <= 65:
                    cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                

    cv2.imshow("Output", frame) 
    cv2.imshow("Paint", paintWindow)
=======
import time
import sqlite3
import os
import uuid


import tkinter as tk
from PIL import Image, ImageTk
from tkinter import simpledialog


# Function to insert images into the database
def insert_image(cur, filename, username):
   with open(filename, 'rb') as input_file:
       ablob = input_file.read()
       base = os.path.basename(filename)
       afile, ext = os.path.splitext(base)
       sql = '''INSERT INTO images1
                 (username,filename, data) VALUES(?,?,?)'''
       cur.execute(sql, (username,afile, sqlite3.Binary(ablob)))
       con.commit()


def lookup_user():
   # Create a new Tkinter window
   root = tk.Tk()
   root.withdraw()  # Hide the main window


   # Ask the user for the username to look up
   lookup_username = ""
   while not lookup_username.strip():
       lookup_username = simpledialog.askstring("Input", "Please enter the username to look up:", parent=root)


   # Look up the user in the database
   cur.execute('''
       SELECT filename, data
       FROM images1
       WHERE username = ?
   ''', (lookup_username,))
   images = cur.fetchall()


   # Display the images
   for filename, data in images:
       with open(filename, 'wb') as output_file:
           output_file.write(data)
       image = cv2.imread(filename)
       cv2.imshow(filename, image)
       cv2.waitKey(0)
       cv2.destroyAllWindows()
       os.remove(filename)




def draw_image():
   root = tk.Tk()
   root.withdraw()  # Hide the main window


   # Ask the user for their username
   username = ""
   while not username.strip():
       username = simpledialog.askstring("Input", "Please enter your username:", parent=root)


   countdown_time = 15
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
   paintWindow = cv2.rectangle(paintWindow, (40,1), (140,65), (0,0,0), 2)
   paintWindow = cv2.rectangle(paintWindow, (160,1), (255,65), (255,0,0), 2)
   paintWindow = cv2.rectangle(paintWindow, (275,1), (370,65), (0,255,0), 2)
   paintWindow = cv2.rectangle(paintWindow, (390,1), (485,65), (0,0,255), 2)
   paintWindow = cv2.rectangle(paintWindow, (505,1), (600,65), (0,255,255), 2)


   # Put the text in for the palette boxes
   cv2.putText(paintWindow, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
   cv2.putText(paintWindow, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
   cv2.putText(paintWindow, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
   cv2.putText(paintWindow, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
   cv2.putText(paintWindow, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
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
   while ret and (username is not None):
       # frame reading
       ret, frame = cap.read()


       # set the current time
       current_time = time.time()
       # Calculate the remaining time
       remaining_time = countdown_time - int(current_time - start_time)
       # Flip the frame vertically
       frame = cv2.flip(frame, 1)
       # Display the remaining time in the top right corner of the frame
       cv2.putText(frame, str(remaining_time), (frame.shape[1] - 50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


       # Check if the countdown has ended
       if remaining_time <= 0:
           filename = "paintWindow"+ str(uuid.uuid4())+".png"
           cv2.imwrite(filename, paintWindow)
           # Store the image in the database
           insert_image(cur,filename,username)
           os.remove(filename)
           cv2.waitKey(0)
          
           cv2.destroyAllWindows()
           cap.release()
           #closes the database
           break
       # change from BGR to RGB values
       framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


       frame = cv2.rectangle(frame, (40,1), (140,65), (0,0,0), 2)
       frame = cv2.rectangle(frame, (160,1), (255,65), (255,0,0), 2)
       frame = cv2.rectangle(frame, (275,1), (370,65), (0,255,0), 2)
       frame = cv2.rectangle(frame, (390,1), (485,65), (0,0,255), 2)
       frame = cv2.rectangle(frame, (505,1), (600,65), (0,255,255), 2)
       cv2.putText(frame, "CLEAR", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
       cv2.putText(frame, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
       cv2.putText(frame, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
       cv2.putText(frame, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
       cv2.putText(frame, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)


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
                   paintWindow[67:,:,:] = 255
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
                   if not center[1] <= 65:
                       cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                  


       cv2.imshow("Output", frame)
       cv2.moveWindow("Output", 650, 0)
       cv2.imshow("Paint", paintWindow)


       if cv2.waitKey(1) == ord('q'):
           break


   #  when q is pressed, exit
   cap.release()
   cv2.destroyAllWindows()


def getoutofprogram():
   #close the database
   con.close()
   exit()


def main_menu():
   # Create a new Tkinter window
   root = tk.Tk()


   # Set the window title
   root.geometry("600x1000")  # Width x Height

   # Create a label with the description
   text1 = "Welcome to our drawing program! Please select an option below.\n 1. Draw an image:\n\n You will be drawing using your palm as a brush, to draw have \na open palm, to no longer draw, close ur open palm\n\n 2. Lookup a user\n\n Using sqlite to search the db for images made by a chosen user\n\n 3. Exit"
   description_label = tk.Label(root, text = text1, justify='center', anchor='center')
   description_label.pack()
   # Create a button for drawing an image
   draw_button = tk.Button(root, text="Draw an image", command=draw_image)
   draw_button.pack()


   # Create a button for looking up a user
   lookup_button = tk.Button(root, text="Lookup a user", command=lookup_user)
   lookup_button.pack()


   # Create a button for exiting the program
   exit_button = tk.Button(root, text="Exit", command=getoutofprogram)
   exit_button.pack()


   # Run the Tkinter event loop
   root.mainloop()


############   end of function definition  ########################


#starting to build the database
con = sqlite3.connect('images.db')
cur = con.cursor()
cur.execute('''
   CREATE TABLE IF NOT EXISTS images1 (
       username TEXT,
       filename TEXT,
       data BLOB
   )
''')
main_menu()
# timer





>>>>>>> Stashed changes:main.py


<<<<<<< Updated upstream:fingerpainter.py
# release the webcam and destroy all active windows
cap.release()
cv2.destroyAllWindows()
=======
>>>>>>> Stashed changes:main.py
