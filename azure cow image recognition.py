# -*- coding: utf-8 -*-
"""
Created on Sat Mar 25 11:52:28 2023

@author: paul2

In this example, we first set up the camera stream using the cv2.VideoCapture() method. Then, we capture each frame from the camera, convert it to a JPEG image, and call the Azure Cognitive Services Computer Vision API to analyze the image for objects. We set the visualFeatures parameter to Objects to request object detection in the image. We loop through the detected objects in the image and check if the object is a cow. If a cow is detected, we print a message to the console. Finally, we display the frame with the detected objects using cv2.imshow() and wait for the 'q' key to be pressed to quit the program.

Note that you will need to replace the <subscription_key> and <endpoint> placeholders with your own subscription key and endpoint URL for the Computer Vision API.
"""

import requests
import json
import cv2
import numpy as np
import time

# Replace <subscription_key> with your own subscription key for Computer Vision API
subscription_key = "<subscription_key>"
# Replace <endpoint> with the endpoint URL for Computer Vision API
endpoint = "<endpoint>"
# Set the API URL for object detection
analyze_url = endpoint + "/vision/v3.2/analyze"

# Set up the camera stream
cap = cv2.VideoCapture(0)

while True:
    # Capture the frame from the camera
    ret, frame = cap.read()

    # Convert the frame to a JPEG image
    ret, buffer = cv2.imencode('.jpg', frame)
    image = buffer.tobytes()

    # Set the parameters for the API call
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,
               'Content-Type': 'application/octet-stream'}
    params = {'visualFeatures': 'Objects'}

    # Call the API to analyze the image
    response = requests.post(analyze_url, headers=headers, params=params, data=image)
    response.raise_for_status()

    # Parse the JSON response
    analysis = response.json()

    # Loop through the detected objects in the image
    for obj in analysis['objects']:
        # Check if the object is a cow
        if obj['object'] == 'cow':
            print('Cow detected!')

    # Display the frame with the detected objects
    cv2.imshow('frame', frame)

    # Wait for 1 millisecond and check for the 'q' key to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
