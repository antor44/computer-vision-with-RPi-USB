#!/usr/bin/env python
"""
Pi Camera Live Image Classification (USB version by Antonio)

Detects objects in continuous stream of images from Pi Camera. Use Edge Impulse
Runner and downloaded .eim model file to perform inference. Bounding box info is
drawn on top of detected objects along with framerate (FPS) in top-left corner.

Author: EdgeImpulse, Inc.
Date: August 3, 2021
License: Apache-2.0 (apache.org/licenses/LICENSE-2.0)
"""

import os, sys, time
import cv2
import numpy as np
from edge_impulse_linux.image import ImageImpulseRunner

# Settings
device = '/dev/video0'                  # Linux video device
model_file = "modelfile.eim"            # Trained ML model from Edge Impulse
res_width = 96                          # Resolution of camera (width)
res_height = 96                         # Resolution of camera (height)
rotation = 0                            # Camera rotation (0, 90, 180, or 270)

# The ImpulseRunner module will attempt to load files relative to its location,
# so we make it load files relative to this program instead
dir_path = os.path.dirname(os.path.realpath(__file__))
model_path = os.path.join(dir_path, model_file)

# Load the model file
runner = ImageImpulseRunner(model_path)

# Initialize model (and print information if it loads)
try:
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
        
        # Convert image to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        
        # Encapsulate raw image values into array for model input
        features, cropped = runner.get_features_from_image(img)
        
        # Perform inference
        res = None
        try:
            res = runner.classify(features)
        except Exception as e:
            print("ERROR: Could not perform inference")
            print("Exception:", e)
            
        # Display predictions and timing data
        print("-----")
        results = res['result']['classification']
        for label in results:
            prob = results[label]
            print(label + ": " + str(round(prob, 3)))
        print("FPS: " + str(round(fps, 3)))
        
        # Find label with the highest probability
        max_label = max(results, key=results.get)
        
        # Draw max label on preview window
        cv2.putText(img,
                    max_label,
                    (0, 12),
                    cv2.FONT_HERSHEY_PLAIN,
                    1,
                    (255, 255, 255))
                    
        # Draw max probability on preview window
        cv2.putText(img,
                    str(round(results[max_label], 2)),
                    (0, 24),
                    cv2.FONT_HERSHEY_PLAIN,
                    1,
                    (255, 255, 255))

        # Convert image to BGR
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
        
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