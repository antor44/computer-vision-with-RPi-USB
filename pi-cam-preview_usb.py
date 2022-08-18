#!/usr/bin/env python
"""
Raspberry Pi Camera Test (USB version by Antonio Ruiz)

Capture frame from Pi Camera and display it to the screen using OpenCV (cv2).
Also display the framerate (fps) to the screen. Use this to adjust the camera's
focus. Press ctrl + c in the console or 'q' on the preview window to stop.

Based on the tutorial from Adrian Rosebrock:
https://www.pyimagesearch.com/2015/03/30/accessing-the-raspberry-pi-camera-with-opencv-and-python/

Author: EdgeImpulse, Inc.
Date: July 5, 2021
License: Apache-2.0 (apache.org/licenses/LICENSE-2.0)
"""


import cv2
import numpy as np
from PIL import Image


# Settings
res_width = 320                         # Resolution of camera (width)
res_height = 320                        # Resolution of camera (height)
rotation = 0                            # Camera rotation (0, 90, 180, or 270)

# Initial framerate value
fps = 0

# Start the camera
camera = cv2.VideoCapture('/dev/video0', cv2.CAP_V4L)
camera.set(cv2.CAP_PROP_FRAME_WIDTH,res_width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT,res_height)

while(True):

        # Acquire frame and expand frame dimensions to have shape: [1, None, None, 3]
        # i.e. a single-column array, where each item in the column has the pixel RGB value
        ret, img = camera.read()

        # Get timestamp for calculating actual framerate
        timestamp = cv2.getTickCount()
        
               
        # Draw framerate on frame
        cv2.putText(img, 
                    "FPS: " + str(round(fps, 2)), 
                    (0, 12),
                    cv2.FONT_HERSHEY_PLAIN,
                    1,
                    (255, 255, 255))
        
        # Show the frame

        cv2.imshow("Frame", img)
        
        
        # Calculate framerate
        frame_time = (cv2.getTickCount() - timestamp) / cv2.getTickFrequency()
        fps = 1 / frame_time
        
        # Press 'q' to quit
        if cv2.waitKey(1) == ord('q'):
            break


camera.release()


cv2.destroyAllWindows()
