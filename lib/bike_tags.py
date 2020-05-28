import re
import logging

import praw

import client
import leaderboard


SUBREDDIT = 'bikeLA'
PHOTOTAG_WIKI = 'phototag'
START_TAG = 291
END_TAG = 388


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


def get_tags(start, end, subreddit):
    """Return dict in format {tag: user}.

    Params:
        start: tag number (int)
        end: tag number (int)
        subreddit: praw Subreddit instance
    """
    tags = {}

    for n in range(start, end) :
        try:
            tags[n] = tag_user(subreddit, n)
        except StopIteration as e:
            logging.info(f'Unable to find tag for #{n}. Skipping')

    return tags


def tag_user(subreddit, tag):
    """Return info for a tag number.

    Params:
        subreddit: praw Subreddit instance
        tag: int
    """
    posts = subreddit.search(tag_str(tag))
    tag_title = [p.title for p in posts if tag_str(tag) in p.title]
    post = next(subreddit.search(tag_title))
    post_author = post.author.name

    return post.author.name


def tag_str(num):
    return f'#{num}'


if __name__ == '__main__':
    client_config = client.get_client_credentials()
    reddit = reddit_client(client_config)
    subreddit = reddit.subreddit(SUBREDDIT)

    new_tags = get_tags(START_TAG, END_TAG, subreddit)
    current_leaderboard = leaderboard.read_existing_leaderboard(subreddit, PHOTOTAG_WIKI)

    all_tags = {**new_tags, **current_leaderboard}
    updated_leaderboard = leaderboard.leaderboard(all_tags)
    sorted_leaderboard = leaderboard.sort_leaderboard(updated_leaderboard)

    print(sorted_leaderboard)

    # TODO: check for missing tags


