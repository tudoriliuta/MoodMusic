from __future__ import print_function
import time
import requests
import cv2
import operator
import pandas as pd
import numpy as np

# Import library to display results
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Display images within Jupyter
from rapidconnect import RapidConnect

# Variables
# URL direction to image
urlImage = 'https://raw.githubusercontent.com/Microsoft/ProjectOxford-ClientSDK/master/Face/Windows/Data/detection3.jpg'

_url = 'https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize'
_key = ''  # Here you have to paste your primary key
_maxNumRetries = 10


def processRequest(json, data, headers, params):
    """
    Helper function to process the request to Project Oxford
    Parameters:
    json: Used when processing images from its URL. See API Documentation
    data: Used when processing image read from disk. See API Documentation
    headers: Used to pass the key information and the data type request
    """

    retries = 0
    result = None

    while True:

        response = requests.request('post', _url, json=json, data=data, headers=headers, params=params)

        if response.status_code == 429:

            print("Message: %s" % (response.json()['error']['message']))

            if retries <= _maxNumRetries:
                time.sleep(1)
                retries += 1
                continue
            else:
                print('Error: failed after retrying!')
                break

        elif response.status_code == 200 or response.status_code == 201:

            if 'content-length' in response.headers and int(response.headers['content-length']) == 0:
                result = None
            elif 'content-type' in response.headers and isinstance(response.headers['content-type'], str):
                if 'application/json' in response.headers['content-type'].lower():
                    result = response.json() if response.content else None
                elif 'image' in response.headers['content-type'].lower():
                    result = response.content
        else:
            print("Error code: %d" % (response.status_code))
            print("Message: %s" % (response.json()['error']['message']))

        break

    return result


def renderResultOnImage(result, img):
    """Display the obtained results onto the input image"""

    face_expressions = []
    for currFace in result:
        faceRectangle = currFace['faceRectangle']
        cv2.rectangle(img, (faceRectangle['left'], faceRectangle['top']),
                      (faceRectangle['left'] + faceRectangle['width'], faceRectangle['top'] + faceRectangle['height']),
                      color=(255, 0, 0), thickness=5)

    for currFace in result:
        faceRectangle = currFace['faceRectangle']
        face_expressions.append(currFace['scores'].items())
        currEmotion = max(currFace['scores'].items(), key=operator.itemgetter(1))[0]

        textToWrite = "%s" % (currEmotion)
        cv2.putText(img, textToWrite, (faceRectangle['left'], faceRectangle['top'] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (255, 0, 0), 1)

    return face_expressions

cap = cv2.VideoCapture(0)

#while (True):
# Capture frame-by-frame
ret, frame = cap.read()

headers = dict()
headers['Ocp-Apim-Subscription-Key'] = _key
headers['Content-Type'] = 'application/json'

json = {'url': urlImage}
data = None
params = None

result = processRequest(json, data, headers, params)
if result is not None:
    # Load the original image, fetched from the URL
    arr = np.asarray(bytearray(requests.get(urlImage).content), dtype=np.uint8)
    img = cv2.cvtColor(cv2.imdecode(arr, -1), cv2.COLOR_BGR2RGB)

    allEmotions = renderResultOnImage(result, frame)

    ig, ax = plt.subplots(figsize=(15, 20))
    ax.imshow(frame)

############################
# Append all emotions to a list
list_dict_emotions = []


# Awkward transformation
allEmotionsList = [list(e) for e in list(allEmotions)]

list_all_emotions = [[list(list(i)[j])[0] for j in range(len(i))] for i in allEmotionsList][0]
list_metrics = [[list(list(i)[j])[1] for j in range(len(i))] for i in allEmotionsList]

sum_confidence = sum(np.array(list_metrics)) / len(list_metrics)

dict_emotions = {}
for i in range(len(list_all_emotions)):
    dict_emotions[list_all_emotions[i]] = sum_confidence[i]

# Append to the list with all dictionaries
list_dict_emotions.append(dict_emotions)

print(dict_emotions)