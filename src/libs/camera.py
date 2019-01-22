import cv2
import logging
import time
import ast
import sys
import os 

# Get current working directory
cwd = os.getcwd() 
# Attach the path of the flask folder in the current working directory
sys.path.append(cwd + '/flask_live_charts')
# Import the py script from flask directory. 
#import flask_live_chart as flc
#from flask_live_charts import live_data
from get_face import get_attributes
#from  flask_live_charts/flask_live_charts import live_data

logger = logging.getLogger()
hdlr = logging.FileHandler('./log.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.DEBUG)

KEY = ''  # Replace with a valid Subscription Key here.

BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/'  # Replace with your regional Base URL

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.list_dict_emotions = []
        self.time_steps = 10
       
    def __del__(self):
        self.video.release()


    def get_confidence(self, time_steps, allEmotions):
        """ Compute the confidence across the previous time_steps """

        # List of all 8 emotions 
        list_all_emotions = [e for e in allEmotions[0]['scores']]

        # List of dictionaries with keys and values
        list_metrics = [i['scores'] for i in allEmotions]

        # Confidence average across dictionaries / faces in the image
        sum_confidence = [sum(d[i] for d in list_metrics) / len(list_metrics) for i in list_all_emotions]

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
        #print(final_dict)

        # Gets the most probable emotion across the previous time_steps 
        #overall_sentiment = max(final_dict.items(), key=operator.itemgetter(1))[0]

        return final_dict #overall_sentiment
    
    
    def get_frame(self):
        #personGroupId = 'myfriends'

        success, image = self.video.read()
        ret, jpeg = cv2.imencode('.jpg', image)

        #cv2.imwrite("test.jpg", image)

        jpeg_bytes = jpeg.tobytes()
        #gets a list of the faces it's found in the webcam shot
        out_str = get_attributes(jpeg_bytes)
        steps = self.time_steps
         
        out_dict = ast.literal_eval(out_str)
        
        if len(out_dict) > 0:
            #print "Persisted prediction"
            emotions_dict = self.get_confidence(time_steps=steps, allEmotions=out_dict)
            print('happy', round(100*emotions_dict['happiness'],2))
            # Visulises the mood. 
            #flc.live_data(emotions_dict)


   
        time.sleep(4)
        #send image to API and compare against participants

        return jpeg_bytes
