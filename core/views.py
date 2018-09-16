from django.shortcuts import render, redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import base64
import praw, random
import requests, json


# Create your views here.
def index(request):
    IMAGE_PATH = "photo.png"

    if request.method == 'POST':
        # Get image from request
        image_data = request.POST.get('image')

        # Write image to file
        fh = open(IMAGE_PATH, "wb")
        fh.write(base64.b64decode(image_data[23:]))
        fh.close()

        # Get emotion, phrase and content url
        emotion = image_to_emotion(IMAGE_PATH)
        print(emotion)
        emotion_phrase = emotion_to_phrases(emotion)
        print(emotion_phrase)
        reddit_url = emotion_to_url(emotion)
        print(reddit_url)

        emotion_session = request.session.get('emotion_session', emotion)
        emotion_phrase_session = request.session.get('emotion_phrase_session', emotion_phrase)
        reddit_url_session = request.session.get('reddit_url_session', reddit_url)

        request.session['emotion_session'] = emotion
        request.session['emotion_phrase_session'] = emotion_phrase
        request.session['reddit_url_session'] = reddit_url

        # Render page and pass path to inage.as context./
        return render(request, 'core/index.html', {
            'emotion': emotion,
            'emotion_phrase': emotion_phrase,
            'reddit_url': reddit_url,
        })

    emotion_session = request.session.get('emotion_session', ' ')
    emotion_phrase_session = request.session.get('emotion_phrase_session', ' ')
    reddit_url_session = request.session.get('reddit_url_session', ' ')

    print(emotion_session)
    print(emotion_phrase_session)
    print(reddit_url_session)

    return render(request, 'core/index.html', {
        'emotion': emotion_session,
        'emotion_phrase': emotion_phrase_session,
        'reddit_url': reddit_url_session,
    })

############# AZURE
# Azure
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
                'happiness': ['aaa'],
                'neutral': ['aaa'],
                'sadness': ['aaa'],
                'surprise': ['aasdasdaa'], }

    return phrases[emotion][random.randint(0, len(phrases[emotion]) - 1)]

def emotion_to_url(emotion):
    emotions = {'anger': 'fml',
                'contempt': 'wholesomememes',
                'disgust': 'facepalm',
                'fear': 'holdmybeer',
                'happiness': 'wholesomememes',
                'neutral': 'me_irl',
                'sadness': 'wholesomememes',
                'surprise': 'wholesomememes', }

    submissions = []

    for post in reddit.subreddit(emotions[emotion]).top("week", limit=30):
        submissions.append(post.url)

    for index, submission in enumerate(submissions):
        if submission[:-4] not in ['jpg', 'jpeg', 'png', 'PNG']:
            submissions.remove(submission)

    print(submissions)
    chosen_submission = random.choice(submissions)
    return chosen_submission



###################

# Image uploading
def upload_image(request):
    IMAGE_PATH = "photo.png"

    if request.method == 'POST':
        # Get image from request
        image_data = request.POST.get('image')

        # Write image to file
        fh = open(IMAGE_PATH, "wb")
        fh.write(base64.b64decode(image_data[23:]))
        fh.close()

        # Get emotion, phrase and content url
        emotion = image_to_emotion(IMAGE_PATH)
        print(emotion)
        emotion_phrase = emotion_to_phrases(emotion)
        print(emotion_phrase)
        reddit_url = emotion_to_url(emotion)
        print(reddit_url)

        emotion_session = request.session.get('emotion_session', emotion)
        emotion_phrase_session = request.session.get('emotion_phrase_session', emotion_phrase)
        reddit_url_session = request.session.get('reddit_url_session', reddit_url)

        request.session['emotion_session'] = emotion
        request.session['emotion_phrase_session'] = emotion_phrase
        request.session['reddit_url_session'] = reddit_url

        # Render page and pass path to inage.as context./
        return render(request, 'core/index.html', {
            'emotion': emotion,
            'emotion_phrase': emotion_phrase,
            'reddit_url': reddit_url,
        })

    emotion_session = request.session.get('emotion_session', ' ')
    emotion_phrase_session = request.session.get('emotion_phrase_session', ' ')
    reddit_url_session = request.session.get('reddit_url_session', ' ')

    print(emotion_session)
    print(emotion_session)
    print(emotion_session)

    return render(request, 'core/index.html', {
        'emotion': emotion_session,
        'emotion_phrase': emotion_phrase_session,
        'reddit_url': reddit_url_session,
    })
