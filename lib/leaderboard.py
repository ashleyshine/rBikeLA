import collections
import re

import praw


def read_existing_leaderboard_tags(subreddit, phototag_wiki):
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

    leaderboard_with_users_combined = combine_identical_users(leaderboard)

    return leaderboard_with_users_combined


def sort_leaderboard(leaderboard):
    """Return leaderboard dict sorted in descending order of num_tags.

    Params:
        leaderboard: dict in form of {user: num_tags}
    """
    sorted_leaderboard = {
        user: num_tags for user, num_tags
        in sorted(leaderboard.items(), key=lambda item: item[1], reverse=True)
    }

    return sorted_leaderboard


def combine_identical_users(leaderboard):
    """Return leaderboard dict with identical users combined. Makes leaderboard
        case insensitive.

    Params:
        leaderboard: dict in form of {user: num_tags}
    """
    users_to_combine = users_with_multiple_names(leaderboard)

    for user in users_to_combine:
        user_names = all_user_names(leaderboard, user)
        to_keep = name_to_keep(user_names, user)
        to_drop = names_to_drop(user_names, to_keep)

        for name in to_drop:
            leaderboard[to_keep] += leaderboard[name]
            leaderboard.pop(name)

    return leaderboard


def users_with_multiple_names(leaderboard):
    """Return list of usernames that appear multiple times in leaderboard.

    Params:
        leaderboard: dict in form of {user: num_tags}
    """
    lowercase_users = [u.lower() for u in leaderboard.keys()]
    user_counts = collections.Counter(lowercase_users)
    users_with_multiple_names = [
        user for user, count
        in collections.Counter(lowercase_users).items() if count > 1
    ]

    return users_with_multiple_names


def all_user_names(leaderboard, user):
    """Return list of all the usernames that appear for a given user in the leaderboard.

    Params:
        leaderboard: dict in form of {user: num_tags}
        user: str
    """
    return [u for u in leaderboard.keys() if u.lower() == user.lower()]


def name_to_keep(all_user_names, user):
    """Return the username to keep for a user whose name appears multiple times (str).
        Prefers names that are not completely lowercase.

    Params:
        all_user_names: list with all the occurences of a user's username
        user: str
    """
    return [u for u in all_user_names if u != u.lower()][0]


def names_to_drop(all_user_names, name_to_keep):
    """Return list of the names to drop for a given user.

    Params:
        all_user_names: list with all the occurences of a user's username
        name_to_keep: str
    """
    return [n for n in all_user_names if n != name_to_keep]


def last_leaderboard_tag(tags):
    return max(tags.keys())


def format_new_leaderboard(leaderboard):
    # TODO: output Tag(link) - found by (link)
    # Modify `get_tags` to return link to post
    return None