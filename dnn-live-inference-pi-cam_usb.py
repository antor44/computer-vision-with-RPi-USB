#!/usr/bin/env python
"""
Raspberry Pi Live Image Inference (USB version by Antonio)

Continuously captures image from Raspberry Pi Camera module and perform 
inference using provided .eim model file. Outputs probabilities in console.

Author: EdgeImpulse, Inc.
Date: June 8, 2021
License: Apache-2.0 (apache.org/licenses/LICENSE-2.0)
"""

import os, sys, time
import cv2
import numpy as np
from edge_impulse_linux.runner import ImpulseRunner

# Settings
device = '/dev/video0'                  # Linux video device
model_file = "modelfile.eim"            # Trained ML model from Edge Impulse
draw_fps = True                         # Draw FPS on screen
res_width = 96                          # Resolution of camera (width)
res_height = 96                         # Resolution of camera (height)
rotation = 0                            # Camera rotation (0, 90, 180, or 270)
img_width = 28                          # Resize width to this for inference
img_height = 28                         # Resize height to this for inference

# The ImpulseRunner module will attempt to load files relative to its location,
# so we make it load files relative to this program instead
dir_path = os.path.dirname(os.path.realpath(__file__))
model_path = os.path.join(dir_path, model_file)

# Load the model file
runner = ImpulseRunner(model_path)

# Initialize model
try:

    # Print model information
    model_info = runner.init()
    print("Model name:", model_info['project']['name'])
    print("Model owner:", model_info['project']['owner'])
    
# Exit if we cannot initialize the model
except Exception as e:
    print("ERROR: Could not initialize model")
    print("Exception:", e)
    if (runner):
            runner.stop()
    sys.exit(1)
    
# Initial framerate value
fps = 0



# Start the camera
camera = cv2.VideoCapture(device, cv2.CAP_V4L)
camera.set(cv2.CAP_PROP_FRAME_WIDTH,res_width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT,res_height)
camera.set(cv2.CAP_PROP_MODE, 0) # CV_CAP_MODE_BGR

# Initial countdown timestamp
countdown_timestamp = cv2.getTickCount()


while(True):
    
        # Acquire frame and expand frame dimensions to have shape: [1, None, None, 3]
        # i.e. a single-column array, where each item in the column has the pixel RGB value
        ret, frame = camera.read()

        # rotate image
        if rotation == 90:
            attr = 'ROTATE_90_CLOCKWISE'
        elif rotation == 180:
            attr = 'ROTATE_180'
        elif rotation == 270:
            attr = 'ROTATE_90_COUNTERCLOCKWISE'

        if rotation > 0:
                frame = cv2.rotate(frame, getattr(cv2, attr))

                                            
        # Get timestamp for calculating actual framerate
        timestamp = cv2.getTickCount()
        
        # Get Numpy array that represents the image

        img = np.array(frame)

        # Crop image (for USB cameras)

        center = img.shape
        x = int(center[1]/2 - res_width/2)
        y = int(center[0]/2 - res_height/2)


        img = img[y:y+res_height, x:x+res_width]

        
        # Resize captured image
        img_resize = cv2.resize(img, (img_width, img_height))
        
        # Convert image to grayscale
        img_resize = cv2.cvtColor(img_resize, cv2.COLOR_BGR2GRAY)
        
        # Convert image to 1D vector of floating point numbers
        features = np.reshape(img_resize, (img_width * img_height)) / 255
        
        # Edge Impulse model expects features in list format
        features = features.tolist()
        
        # Perform inference
        res = None
        try:
            res = runner.classify(features)
        except Exception as e:
            print("ERROR: Could not perform inference")
            print("Exception:", e)
            
        # Display predictions and timing data
        print("Output:", res)
        
        # Display prediction on preview
        if res is not None:
        
            # Find label with the highest probability
            predictions = res['result']['classification']
            max_label = ""
            max_val = 0
            for p in predictions:
                if predictions[p] > max_val:
                    max_val = predictions[p]
                    max_label = p
                    
            # Draw predicted label on bottom of preview
            cv2.putText(img,
                        max_label,
                        (0, res_height - 20),
                        cv2.FONT_HERSHEY_PLAIN,
                        1,
                        (255, 255, 255))
                        
            # Draw predicted class's confidence score (probability)
            cv2.putText(img,
                        str(round(max_val, 2)),
                        (0, res_height - 2),
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

        # Show the frame
        cv2.imshow("Frame", img)
        
        
        # Calculate framrate
        frame_time = (cv2.getTickCount() - timestamp) / cv2.getTickFrequency()
        fps = 1 / frame_time
        
        # Press 'q' to quit
        if cv2.waitKey(1) == ord('q'):
            break

camera.release()

            
# Clean up
cv2.destroyAllWindows()

