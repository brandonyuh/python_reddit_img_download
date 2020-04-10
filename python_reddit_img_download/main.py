import sys

import reddit_variables
import praw
import re
import pyperclip
import requests

# Replace with your own at https://www.reddit.com/prefs/apps
client_id = reddit_variables.client_id
client_secret = reddit_variables.client_secret
user_agent = reddit_variables.user_agent

reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

regex_url = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

def main():
    url = pyperclip.paste()
    if (not re.match(regex_url, url)):
        url = sys.argv[1]
        if (not re.match(regex_url, url)):
            url = input("URL?")
            if (not re.match(regex_url, url)):
                print("URL invalid quitting")
                sys.exit(1)

    submission = reddit.submission(url=url)
    author = str(submission.author)
    image_url = submission.url
    id = str(submission.id)

    local_image = author + "_" + id + ".png"
    with open(author + "_" + id + ".txt", "w") as file:
        file.write(url)
    img_data = requests.get(image_url).content
    with open(local_image, 'wb') as handler:
        handler.write(img_data)

if __name__ == "__main__":
    main()