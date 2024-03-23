import pygsheets
import random
from decouple import config
import os
import time
import requests
from requests_oauthlib import OAuth1


dir = "/home/chaoticneuron/SamvidhanBot"
dir = os.getcwd()
def tweet_viveka_wisdom():

    consumer_key = config('consumer_key')
    consumer_secret = config('consumer_secret')
    access_token = config('access_token')
    access_token_secret = config('access_token_secret')

    oauth = OAuth1(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret
        )

    # Twitter API endpoints
    tweet_url = 'https://api.twitter.com/2/tweets'
    media_upload_url = 'https://upload.twitter.com/1.1/media/upload.json'

    # MAKE TWEET
    gc = pygsheets.authorize(service_file=dir+r'/constitutionbot-3e833b17dba1.json')
    sh = gc.open('Vivekam')
    wks = sh.worksheet('title', 'Sheet1')
    df = wks.get_as_df()
    df = df[(df['Length'] <= 280) & (df['Length'] > 0)].reset_index(drop=True)
    n = random.randint(0, df.shape[0] - 1)
    
    files = os.listdir(dir+r'/Media/')
    k = random.randint(0, len(files)-1)
    author_image = files[k]

    tweet = str(df['Tweet'][n])

    image_path = dir+r'/Media/'+author_image
    files = {'media': (author_image+'.jpg', open(image_path, 'rb'))}
    media_response = requests.post(media_upload_url, auth=oauth, files=files)
    media_id = media_response.json()['media_id_string']

    tweet_data = {
        'text': tweet,
        'media': {'media_ids':[media_id]}
                        }

    #print(type(df['Author'][n]))
    #print(author_image)
    #print(tweet)
    # Upload the image

    
    # Making the request
    tweet_response = requests.post(tweet_url, auth=oauth, json=tweet_data)


def run():
    while True:
        tweet_viveka_wisdom()
        time.sleep(3600)

if __name__ == "__main__":
    run()
