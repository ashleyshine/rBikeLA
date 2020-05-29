import json

import praw

CLIENT_PATH = '../config/client'


def get_client_credentials():
    with open(CLIENT_PATH, 'r') as f:
        credentials = json.loads(f.read())

    return credentials


def reddit_client(config):
    """Return praw Reddit instance.

    Params:
        config: dict containing client info
    """
    client = praw.Reddit(
        client_id = config['client_id'],
        client_secret = config['client_secret'],
        user_agent = config['user_agent']
    )

    return client


def get_subreddit(subreddit):
    """Return praw Subreddit instance
    """
    client_config = get_client_credentials()
    reddit = reddit_client(client_config)
    subreddit = reddit.subreddit(subreddit)

    return subreddit
