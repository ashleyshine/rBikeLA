import collections
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


def leaderboard(tags):
    """Return dict in form of {user: num_tags}.

    Params:
        tags: dict in form of {tag: user}
    """
    leaderboard = collections.defaultdict(int)

    for user in tags.values():
        leaderboard[user] += 1

    return leaderboard


def sort_leaderboard(leaderboard):
    """Return leaderboard dict sorted in descending order of num_tags.

    Params:
        leaderboard: dict in form of {user:num_tags}
    """
    sorted_leaderboard = {
        user: num_tags for user, num_tags
        in sorted(leaderboard.items(), key=lambda item: item[1], reverse=True)
    }

    return sorted_leaderboard


def format_new_leaderboard(leaderboard):
    # TODO: output Tag(link) - found by (link)
    # Modify `get_tags` to return link to post
