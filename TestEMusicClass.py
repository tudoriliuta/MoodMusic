from __future__ import print_function
import time 
import requests
import cv2
import operator
import pandas as pd
import numpy as np
import http.client, urllib.request, urllib.parse, urllib.error, base64

# Import library to display results
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Display images within Jupyter
from rapidconnect import RapidConnect

# Variables
# URL direction to image
class GetImageSentiment:
    def __init__(self, urlImage, time_steps):
        self.urlImage = urlImage
        self.time_steps = time_steps
        self.list_dict_emotions = []
        self.allEmotions = None

    ############################
    # Append all emotions to a list
    _url = 'https://westus.api.cognitive.microsoft.com/emotion/v1.0/recognize'
    _key = '' #Here you have to paste your primary key
    _maxNumRetries = 10

    def processRequest(json, data, headers, params ):

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

            response = requests.request( 'post', _url, json = json, data = data, headers = headers, params = params )

            if response.status_code == 429: 

                print( "Message: %s" % ( response.json()['error']['message'] ) )

                if retries <= _maxNumRetries: 
                    time.sleep(1) 
                    retries += 1
                    continue
                else: 
                    print( 'Error: failed after retrying!' )
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
                print( "Error code: %d" % ( response.status_code ) )
                print( "Message: %s" % ( response.json()['error']['message'] ) )

            break
            
        return result


    def renderResultOnImage(result, img):
        """Display the obtained results onto the input image"""
        
        face_expressions = []
        for currFace in result:
            faceRectangle = currFace['faceRectangle']
            cv2.rectangle( img,(faceRectangle['left'],faceRectangle['top']),
                               (faceRectangle['left']+faceRectangle['width'], faceRectangle['top'] + faceRectangle['height']),
                           color = (255,0,0), thickness = 5 )


        for currFace in result:
            faceRectangle = currFace['faceRectangle']
            face_expressions.append(currFace['scores'].items())
            currEmotion = max(currFace['scores'].items(), key=operator.itemgetter(1))[0]


            textToWrite = "%s" % ( currEmotion )
            cv2.putText(img, textToWrite, (faceRectangle['left'],faceRectangle['top']-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,0,0), 1 )
            
        return face_expressions

    """headers = dict()
    headers['Ocp-Apim-Subscription-Key'] = _key
    headers['Content-Type'] = 'application/json' 

    json = { 'url': urlImage } 
    data = None
    params = None

    result = processRequest(json, data, headers, params)

    if result is not None:
        # Load the original image, fetched from the URL
        arr = np.asarray( bytearray( requests.get(urlImage).content ), dtype=np.uint8 )
        img = cv2.cvtColor( cv2.imdecode( arr, -1 ), cv2.COLOR_BGR2RGB )

        self.allEmotions = renderResultOnImage(result, img)

        ig, ax = plt.subplots(figsize=(15, 20))
        ax.imshow(img)
    """

    headers = {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': 'cc2b2790ff6c41688925e9778b1cd58e',
    }

    params = urllib.parse.urlencode({
    })

    # Replace the example URL below with the URL of the image you want to analyze.
    #body = "{ 'url': 'http://example.com/picture.jpg' }"
    _, jpeg = cv2.imencode('.jpg', img)
    body=jpeg.tobytes()
    try:
        # NOTE: You must use the same region in your REST call as you used to obtain your subscription keys.
        #   For example, if you obtained your subscription keys from westcentralus, replace "westus" in the 
        #   URL below with "westcentralus".
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()
        get_confidence(10, data)
        conn.close()
    except Exception as e:
        print(e.args)



    def get_confidence(time_steps, allEmotions):
        """ Compute the confidence across the previous time_steps """

        # Awkward transformation of the microsoft visual api to a list of confidence values / emotions
        allEmotionsList = [list(e) for e in list(allEmotions)]

        list_all_emotions = [[list(list(i)[j])[0] for j in range(len(i))] for i in allEmotionsList][0]
        list_metrics = [[list(list(i)[j])[1] for j in range(len(i))] for i in allEmotionsList]

        sum_confidence = sum(np.array(list_metrics)) / len(list_metrics)

        # Converts the confidence vector to a dictionary
        dict_emotions = {}
        for i in range(len(list_all_emotions)):
            dict_emotions[list_all_emotions[i]] = sum_confidence[i]

        # Append the dictionary to the list with all dictionaries
        self.list_dict_emotions.append(dict_emotions)

        # Gets top time_steps entries in the emotions list. 
        last_five_entries = self.list_dict_emotions[-time_steps:]

        # Get the average across the previous time_steps entries, as a vector of confidence scores. 
        last_five_entries_avg = [float(sum(d[j] for d in self.list_dict_emotions)) / len(self.list_dict_emotions) for j in list_all_emotions]

        # Builds the returned vector into a final dictionary with emotions as labels and confidence as values
        final_dict = {}

        for i in range(len(list_all_emotions)):
            final_dict[list_all_emotions[i]] = last_five_entries_avg[i]

        # Prints the result
        print(final_dict)

        # Gets the most probable emotion across the previous time_steps 
        overall_sentiment = max(final_dict.items(), key=operator.itemgetter(1))[0]

        return overall_sentiment



