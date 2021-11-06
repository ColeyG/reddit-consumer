import praw
import os.path
import yaml

# Stinky Globals
postHintTypes = []
successfulResults = 0
configurationFileName = "configuration.yaml"

# Check for configuration before launching
if os.path.isfile(configurationFileName):
    config = yaml.safe_load(open(configurationFileName))
else:
    raise Exception(
        'Will not run without a configuration file, copy configuration-example.yaml and replace its values.')
    # TODO: Instead also check for args and pass them in

# Configuration Variables
subreddits = config['subreddits']
amountOfResults = config['amount']
filterStickied = True

# TODO: check args for missing configuration here

# API Configuration
reddit = praw.Reddit(
    client_id=config['id'],
    client_secret=config['secret'],
    user_agent=config['userAgent']
)


def check_stickied(post):
    return not post.stickied


def print_postdata(post):
    print("-Praw Post---------------")
    print(post.title.encode("utf-8"))
    print("URL: " + post.url)
    print("ID: " + post.id)
    if hasattr(post, 'post_hint'):
        print("Hint: " + post.post_hint)
    else:
        print("Hint: no hint")
    print("-------------------------")


def save_post(post):
    postMetaJson = '{"id":"' + post.id + '","url":"' + post.url + '"}'

    open("data/meta/" + post.id + ".json",
         "wb").write(postMetaJson.encode("utf-8"))

    # open("data/postdata/" + post.id + ".json",
    #      "wb").write(post) TODO: Make this work


def request(amount=10, subreddit="all"):
    posts = reddit.subreddit(subreddit).hot(limit=amount)

    if filterStickied:
        posts = filter(check_stickied, posts)

    for post in posts:
        if hasattr(post, 'post_hint'):
            if post.post_hint not in postHintTypes:
                postHintTypes.append(post.post_hint)
        print_postdata(post)
        save_post(post)


def main():
    for subreddit in subreddits:
        request(amount=amountOfResults, subreddit=subreddit)
    print("--Finished---------------")
    print("Successful Downloads: " + str(successfulResults))
    print("Post Hint Types: " + str(postHintTypes))
    print("-------------------------")


main()
