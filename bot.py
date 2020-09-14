import json
import time
import requests
import tweepy

#-----------------------------------------------------------------------------------------#

twitAPIKey = 'xxxxx'
twitAPISecretKey = 'xxxxx'
twitAccessToken = 'xxxxx'
twitAccessTokenSecret = 'xxxxx'

delay = 5

#-----------------------------------------------------------------------------------------#

print("STARTING BOT...")

auth = tweepy.OAuthHandler(twitAPIKey, twitAPISecretKey)
auth.set_access_token(twitAccessToken, twitAccessTokenSecret)
api = tweepy.API(auth)

count = 1
while 1:
    with open('news.json', 'r', encoding="utf8") as file:
        old = json.load(file)
        try:
            req = requests.get(f"https://fortnite-api.com/v2/news/br?lang=en")
            if req.status_code != 200:
                pass
            new = req.json()
        except:
            pass



    print(f'Checking for news update: {count}')
    count = count + 1

    if old != new:

        try:
            for i in new["data"]["motds"]:
                if not i in old["data"]["motds"]:

                    r = requests.get(i["image"], allow_redirects=True)
                    open(f'NewsImages/{i["id"]}.jpg', 'wb').write(r.content)

                    id = i["id"]
                    title = i["title"]
                    body = i["body"]

                    try:
                        api.update_with_media(f"NewsImages/{id}.jpg",f"#Fortnite News Update:\n\n{title}\n\n{body}")
                        print(f"Tweeted news feed! ({id})")
                    except:
                        print("Failed to tweet news feed")
        except:
            pass
        with open('news.json', 'w', encoding="utf8") as file:
            json.dump(new, file, indent=3)

    time.sleep(delay)
