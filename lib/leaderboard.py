import re

import praw


def read_existing_leaderboard(subreddit, phototag_wiki):
    """Read the existing leaderboard in the phototag wiki.

    Params:
        subreddit: praw Subreddit instance
        phototag_wiki: name of the phototag (rules) wiki (str)
    """
    wiki = subreddit.wiki[phototag_wiki]
    wiki_lines = wiki.content_md.split('\n')

    tags = {}

    for line in wiki_lines:
        tag_line = match_tag_line(line)
        if tag_line:
            tag = tag_line.group(1)
            user = tag_line.group(2)
            tags[int(tag)] = user.strip('*\r')

    return tags


def match_tag_line(line):
    """Return re Match object if the line contains a tag.

    Params:
        line: str
    """
    return re.search(r'\[Tag #(\d+)\].*found by /u/(.*)', line)


def get_top_N_taggers(tags, N):
    # TODO
    # ignore case when combining tags
    return None
