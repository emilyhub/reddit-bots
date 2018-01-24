import praw, config
import requests, os

def bot_login():
    r = praw.Reddit(username = config.username,
                password = config.password,
                client_id = config.client_id,
                client_secret = config.client_secret,
                user_agent = "Joke comment responder")
    print("Logged in")
    return r

def run_bot(r, comments_replied_to):
    print("Getting the 25 newest comments")
    for comment in r.subreddit("test").comments(limit=25):
        if "chuck" in comment.body and comment.id not in comments_replied_to:
            print("\"chuck\" found in comment " + comment.id)
            comment_reply = "Here is a Chuck Norris joke:\n\n"
            joke = requests.get("http://api.icndb.com/jokes/random").json()['value']['joke']
            comment_reply += ">" + joke
            comment_reply += "\n\nThis joke came from [ICNDB](http://icndb.com)."
            comment.reply(comment_reply)
            print("Replied to comment " + comment.id)

            comments_replied_to.append(comment.id)
            with open("comments_replied_to.txt", "a") as f:
                f.write(comment.id + "\n")

def get_saved_comments():
    if not os.path.isfile("comments_replied_to.txt"):
        comments_replied_to = []
    else:
        with open("comments_replied_to.txt", "r") as f:
            comments_replied_to = f.read()
            comments_replied_to = comments_replied_to.split("\n")
    return comments_replied_to


r = bot_login()
comments_replied_to = get_saved_comments()
run_bot(r, comments_replied_to)