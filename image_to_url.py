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


def emotion_to_url(emotion):
    emotions = {'anger': None, 'contempt': None, 'disgust': None, 'fear': 'getmotivated', 'happiness': None, 'neutral': None, 'sadness': 'wholesomememes', 'surprise': None, }
    submissions = []

    for post in reddit.subreddit(emotions[emotion]).top("week", limit=10):
        submissions.append(post.url)
    return submissions[random.randint(0, 9)]

def image_to_emotion(image_url):
    headers = {'Ocp-Apim-Subscription-Key': subscription_key}
    params = {'returnFaceAttributes':'emotion'}
    data = {'url': image_url}
    response = requests.post(face_api_url, params=params, headers=headers, json=data)
    faces = response.json()[0]['faceAttributes']['emotion'] # Contains all the emotions with percentages on which is most likely
    return max(faces, key=faces.get) #Returns the key with the highest value

if __name__ == "__main__":
    image_url = 'https://amp.businessinsider.com/images/506f1690eab8eaef04000004-750-563.jpg'
    emotion = image_to_emotion(image_url)
    print(emotion)
    print(emotion_to_url(emotion))
