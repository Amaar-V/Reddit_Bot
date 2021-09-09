import webbrowser
import praw
import os
import random
import urllib.request
import requests
from bs4 import BeautifulSoup

reddit = praw.Reddit('bot1')

if not os.path.isfile("posts_replied_to.txt"):
    posts_replied_to = []

else:
    with open("posts_replied_to.txt", "r") as f:
        posts_replied_to = f.read()
        posts_replied_to = posts_replied_to.split("\n")
        posts_replied_to = list(filter(None, posts_replied_to))

sneak_replies = \
    [
        "Hi, my name is Sneaker_Bot.",
        "Hello, my name is Sneaker_Bot and I am here to ID sneakers.",
        "Hey, I'm Sneaker_Bot!",
        "It's time to ID sneakers and chew bubblegum and I'm all out of bubblegum."
    ]

subreddit = reddit.subreddit('Sneaker_Bot')


def find(results):
    s = results[0].get('title')
    z = False
    y = False
    b = True
    if s.find("-") != -1:
        z = True
    if s.find("(") != -1:
        y = True
    if z:
        if y:
            if s.find("(") < s.find("-"):
                b = False
    if z & b:
        s = s[0: s.find("-") - 1]
        s.strip()
        s.lower()
        a = 0
        for x in results:
            e = x.get('title')
            if e.find("-") != -1:
                e = e[0: e.index("-") - 1]
                e.strip()
                e.lower()
                if s == e:
                    a = a + 1
        if a > 1:
            return s
        else:
            iden = results[0].get('title').split()
            return iden[0] + " " + iden[1]

    elif y:
        s = s[0: s.find("(") - 1]
        s.strip()
        s.lower()
        a = 0
        for x in results:
            e = x.get('title')
            if e.find("(") != -1:
                e = e[0: e.index("(") - 1]
                e.strip()
                e.lower()
                if s == e:
                    a = a + 1
        if a > 1:
            return s
        else:
            iden = results[0].get('title').split()
            return iden[0] + " " + iden[1]
    else:
        iden = results[0].get('title').split()
        return iden[0] + " " + iden[1]


def correctPrecentage(results):
    s = results[0].get('title')
    z = False
    y = False
    if s.find("-") != -1:
        z = True
    if s.find("(") != -1:
        y = True
    if z:
        s = s[0: s.find("-") - 1]
        a = 0
        for x in results:
            e = x.get('title')
            if e.find("-") != -1:
                e = e[0: e.index("-") - 1]
                if s == e:
                    a = a + 1
        if a > 1:
            return a
        else:
            return 0
    elif y:
        s = s[0: s.find("(") - 1]
        a = 0
        for x in results:
            e = x.get('title')
            if e.find("(") != -1:
                e = e[0: e.index("(") - 1]
                if s == e:
                    a = a + 1
        if a > 1:
            return a
        else:
            return 0
    else:
        return 0


for submission in subreddit.hot(limit=1):
    if submission.id not in posts_replied_to:
        # if re.search("f", submission.title, re.IGNORECASE):
        sneak_reply = random.choice(sneak_replies)
        urllib.request.urlretrieve(submission.url, "testImages/sneaker"+submission.id+".jpg")
        filePath = 'testImages/sneaker'+submission.id+'.jpg'
        searchUrl = 'http://www.google.hr/searchbyimage/upload'
        multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}
        response = requests.post(searchUrl, files=multipart, allow_redirects=False)
        fetchUrl = response.headers['Location']
        webbrowser.open(fetchUrl)
        URL = fetchUrl
        # desktop user-agent
        USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:65.0) Gecko/20100101 Firefox/65.0"
        headers = {"user-agent": USER_AGENT}
        resp = requests.get(URL, headers=headers)
        results = []
        #print("status code: " + resp.status_code + "\n")
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.content, "html.parser")
            for g in soup.find_all('div', class_='r'):
                anchors = g.find_all('a')
                if anchors:
                    link = anchors[0]['href']
                    title = g.find('h3').text
                    item = {
                        "title": title,
                        "link": link
                    }
                    results.append(item)
            print(results)
            print(correctPrecentage(results))
            sneak_reply += "\nI believe this sneaker to be: " + find(results) + "\n with a " \
                           + format((correctPrecentage(results) / len(results) * 100), '.0f') + "% likelihood. "
            sneak_reply += "The link for this is: " + results[0].get('link')
        reddit = praw.Reddit('bot1')
        submission.reply(sneak_reply)
        print(sneak_reply)
        print("Bot replying to : ", submission.title)
        posts_replied_to.append(submission.id)

with open("posts_replied_to.txt", "w") as f:
    for post_id in posts_replied_to:
        f.write(post_id + "\n")
