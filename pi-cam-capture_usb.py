#!/usr/bin/env python
"""
Raspberry Pi Camera Image Capture (USB version by Antonio)

Displays image preview on screen. Counts down and saves image. Restart program 
to take multiple photos.

Author: EdgeImpulse, Inc.
Date: July 6, 2021
License: Apache-2.0 (apache.org/licenses/LICENSE-2.0)
"""

import cv2
import numpy as np


# Settings
device = '/dev/video0'                  # Linux video device path
res_width = 96                          # Resolution of camera (width)
res_height = 96                         # Resolution of camera (height)
rotation = 0                            # Camera rotation (0, 90, 180, or 270)
draw_fps = False                        # Draw FPS on screen
save_path = "./"                        # Save images to current directory
file_num = 0                            # Starting point for filename
file_suffix = ".png"                    # Extension for image file
precountdown = 2                        # Seconds before starting countdown
countdown = 5                           # Seconds to count down from

# Initial framerate value
fps = 0

################################################################################
# Functions

def file_exists(filepath):
    """
    Returns true if file exists, false otherwise
    """
    try:
        f = open(filepath, 'r')
        exists = True
        f.close()
    except:
        exists = False
    return exists


def get_filepath():
    """
    Returns the next available full path to image file
    """

    global file_num

    # Loop through possible file numbers to see if that file already exists
    filepath = save_path + str(file_num) + file_suffix
    while file_exists(filepath):
        file_num += 1
        filepath = save_path + str(file_num) + file_suffix

    return filepath

################################################################################
# Main

# Figure out the name of the output image filename
filepath = get_filepath()


# Start the camera
camera = cv2.VideoCapture(device, cv2.CAP_V4L)
camera.set(cv2.CAP_PROP_FRAME_WIDTH,res_width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT,res_height)

# Initial countdown timestamp
countdown_timestamp = cv2.getTickCount()


while(True):

        # Acquire frame and expand frame dimensions to have shape: [1, None, None, 3]
        # i.e. a single-column array, where each item in the column has the pixel RGB value
        ret, img = camera.read()

        # rotate image
        if rotation == 90:
            attr = 'ROTATE_90_CLOCKWISE'
        elif rotation == 180:
            attr = 'ROTATE_180'
        elif rotation == 270:
            attr = 'ROTATE_90_COUNTERCLOCKWISE'

        if rotation > 0:
                img = cv2.rotate(img, getattr(cv2, attr))
                                            
        # Get timestamp for calculating actual framerate
        timestamp = cv2.getTickCount()
       
        # Each second, decrement countdown
        if (timestamp - countdown_timestamp) / cv2.getTickFrequency() > 1.0:
            countdown_timestamp = cv2.getTickCount()
            countdown -= 1
            
            # When countdown reaches 0, break out of loop to save image
            if countdown <= 0:
                countdown = 0
                break
                
        
        # Draw countdown on screen
        cv2.putText(img,
                    str(countdown),
                    (int(round(res_width / 2) - 5),
                        int(round(res_height / 2))),
                    cv2.FONT_HERSHEY_PLAIN,
                    1,
                    (255, 255, 255))
                    
        # Draw framerate on frame
        if draw_fps:
            cv2.putText(img, 
                        "FPS: " + str(round(fps, 2)), 
                        (0, 12),
                        cv2.FONT_HERSHEY_PLAIN,
                        1,
                        (255, 255, 255))

        # Draw rectangle on frame

        img = np.array(img)
        center = img.shape
        x = int(center[1]/2 - res_width/2)
        y = int(center[0]/2 - res_height/2)

        cv2.rectangle(img, pt1=(x,y), pt2=(x+res_width,y+res_height), color=(0,255,0), thickness=1)
        
        # Show the frame
        cv2.imshow("Frame", img)
        
        
        # Calculate framrate
        frame_time = (cv2.getTickCount() - timestamp) / cv2.getTickFrequency()
        fps = 1 / frame_time
        
        # Press 'q' to quit
        if cv2.waitKey(1) == ord('q'):
            break

camera.release()
    


# Capture image

crop_img = img[y:y+res_height, x:x+res_width]

cv2.imwrite(filepath, crop_img)

print("Image saved to:", filepath)


# Clean up
cv2.destroyAllWindows()

