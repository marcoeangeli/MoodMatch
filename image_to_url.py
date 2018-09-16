import praw, random
import requests, json
#import matplotlib.pyplot as plt
#from PIL import Image
#from matplotlib import patches
#from io import BytesIO
subscription_key = "0001d91249d94b83b6eae6973496d0e4"
assert subscription_key
face_api_url = 'https://canadacentral.api.cognitive.microsoft.com/face/v1.0/detect'
reddit = praw.Reddit(client_id="M87nRI3kCjaYRw", client_secret="2-sFdzE_TE58cQTMZwLpxZNiC60", user_agent='Hack the North 2018')

def image_to_emotion(image_path):
    headers = {'Ocp-Apim-Subscription-Key': subscription_key,'Content-Type': 'application/octet-stream'}
    params = {'returnFaceAttributes':'emotion'}

    image_data = open(image_path, "rb").read() # Read the image into a byte array
    response = requests.post(face_api_url, params=params, headers=headers, data=image_data)
    faces = response.json()[0]['faceAttributes']['emotion'] # Contains all the emotions with percentages on which is most likely
    del faces['contempt']
    return max(faces, key=faces.get) #Returns the key with the highest value

def emotion_to_phrases(emotion):
    phrases =  {'anger': ['Why so angry?'],
                'contempt': ['Thats a high horse you are on right now.'],
                'disgust': ['Why so disgusted? Did you look into a mirror?'],
                'fear': ['Wow you are such'],
                'happiness': [],
                'neutral': [],
                'sadness': [],
                'surprise': [], }

    return phrases[emotion][random.randint(0, phrases[emotion].length() - 1)]

def emotion_to_url(emotion):
    emotions = {'anger': None,
                'contempt': None,
                'disgust': None,
                'fear': 'getmotivated',
                'happiness': None,
                'neutral': None,
                'sadness': 'wholesomememes',
                'surprise': None, }

    submissions = []

    for post in reddit.subreddit(emotions[emotion]).top("week", limit=10):
        submissions.append(post.url)
    return submissions[random.randint(0, 9)]

if __name__ == "__main__":
    image_path = "C:/Users/marco/Pictures/Camera Roll/test.jpg"
    emotion = image_to_emotion(image_path)
    print(emotion)
