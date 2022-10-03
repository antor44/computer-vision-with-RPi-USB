#!/usr/bin/env python
"""
Live Object Detection (USB version by Antonio)

Detects objects in continuous stream of images from Pi Camera. Use Edge Impulse
Runner and downloaded .eim model file to perform inference. Bounding box info is
drawn on top of detected objects along with framerate (FPS) in top-left corner.

Author: EdgeImpulse, Inc.
Date: July 5, 2021
License: Apache-2.0 (apache.org/licenses/LICENSE-2.0)
"""

import os, sys, time
import cv2
import numpy as np
from edge_impulse_linux.image import ImageImpulseRunner

# Settings
device = '/dev/video0'                   # Linux video device
model_file = "modelfile.eim"             # Trained ML model from Edge Impulse
cam_width = 640                          # Width of frame (pixels)
cam_height = 480                         # Height of frame (pixels)
res_width = 320                          # Resolution of camera (width)
res_height = 320                         # Resolution of camera (height)
rotation = 0                             # Camera rotation (0, 90, 180, or 270)

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
camera.set(cv2.CAP_PROP_FRAME_WIDTH,cam_width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT,cam_height)
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

        # Crop image

        center = img.shape
        x = int(center[1]/2 - res_width/2)
        y = int(center[0]/2 - res_height/2)

        img = img[y:y+res_height, x:x+res_width]
        
        # Convert to RGB and encapsulate raw values into array for model input
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        features, cropped = runner.get_features_from_image(img_rgb)
        
        # Perform inference
        res = None
        try:
            res = runner.classify(features)
        except Exception as e:
            print("ERROR: Could not perform inference")
            print("Exception:", e)
            
        # Display predictions and timing data
        print("Output:", res)
        
        # Go through each of the returned bounding boxes
        bboxes = res['result']['bounding_boxes']
        for bbox in bboxes:
        
            # Calculate corners of bounding box so we can draw it
            b_x0 = bbox['x']
            b_y0 = bbox['y']
            b_x1 = bbox['x'] + bbox['width']
            b_y1 = bbox['y'] + bbox['height']
            
            # Draw bounding box over detected object
            cv2.rectangle(img,
                            (b_x0, b_y0),
                            (b_x1, b_y1),
                            (255, 255, 255),
                            1)
                            
            # Draw object and score in bounding box corner
            cv2.putText(img,
                        bbox['label'] + ": " + str(round(bbox['value'], 2)),
                        (b_x0, b_y0 + 12),
                        cv2.FONT_HERSHEY_PLAIN,
                        1,
                        (255, 255, 255))
        
        # Draw framerate on frame
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
