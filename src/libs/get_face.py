import http.client, urllib, base64, json


def get_attributes(image):


    ###############################################
    #### Update or verify the following values. ###
    ###############################################

    # Replace the subscription_key string value with your valid subscription key.
    subscription_key = ''

    # Replace or verify the region.
    #
    # You must use the same region in your REST API call as you used to obtain your subscription keys.
    # For example, if you obtained your subscription keys from the westus region, replace 
    # "westcentralus" in the URI below with "westus".
    #
    # NOTE: Free trial subscription keys are generated in the westcentralus region, so if you are using
    # a free trial subscription key, you should not need to change this region.
    uri_base = 'https://westus.api.cognitive.microsoft.com'

    # Request headers.
    headers = {
        'Content-type': 'application/octet-stream',
        #'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    # Request parameters.
    params = urllib.parse.urlencode({})




    # The URL of a JPEG image to analyze.
    #body = "{'url':'https://upload.wikimedia.org/wikipedia/commons/c/c3/RH_Louise_Lillian_Gish.jpg'}"
    body = image
    try:
        # Execute the REST API call and get the response.
        conn = http.client.HTTPSConnection('westus.api.cognitive.microsoft.com')
        conn.request("POST", "/emotion/v1.0/recognize?%s" % params, body, headers)
        response = conn.getresponse()
        data = response.read()

        return data
        conn.close()

    except Exception as e:
        print("[Errno {0}] {1}".format(e.errno, e.strerror))

if __name__=="__main__":
    #body = "{'url':'https://upload.wikimedia.org/wikipedia/commons/c/c3/RH_Louise_Lillian_Gish.jpg'}"
    body = "{ 'url': 'http://www.thesnapsociety.com/wp-content/uploads/2014/05/emotion-briana-burns.jpg' }"
    get_attributes(image=body)
