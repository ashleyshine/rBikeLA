import json
import logging
import os
import re

import pprint

import reddit
import leaderboard
import parser
import qa

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')


SUBREDDIT = 'bikeLA'
PHOTOTAG_WIKI = 'phototag'
RESOURCE_DIR = './resources'
OVERRIDE_FILES = ['conflicting_tags.json', 'missing_tags.json']
DEFAULT_START_TAG = 1


def get_tags(start, end, subreddit, manual_overrides={}):
    """Return dict in format {tag: tag_info}.

    Params:
        start: tag number (int)
        end: tag number (int)
        subreddit: praw Subreddit instance
    """
    tags = {}

    for n in range(start, end + 1):
        try:
            tags[n] = tag_info(subreddit, n, manual_overrides)
            tags[n-1]['location'] = tags[n]['previous_location']
        except Exception as e:
            logging.error(e)

    return tags


def tag_info(subreddit, tag, manual_overrides={}):
    """Return info for a tag number.
    Params:
        subreddit: praw Subreddit instance
        tag: int
    """
    tag_titles = get_tag_posts(subreddit, tag)
    manual_override = has_manual_override(manual_overrides, tag)
    n_posts = len(tag_titles)

    if manual_override:
        logging.info(f'Using manual override for #{tag}.')
        post_info = manual_overrides[tag]
    elif n_posts == 0:
        raise Exception(
            f'No posts found for #{tag}. Skipping.' +
            'Please find post manually and add to resource directory.'
        )
    elif n_posts > 1:
        raise Exception(
            f'More than one post found for #{tag}. Skipping. ' +
            'Please resolve manually and add to resource directory.' +
            '\nTag posts: {tag_titles}'
        )
    else:
        post_info = get_tag_info_from_post(tag_titles[0], tag)

    return post_info


def get_tag_posts(subreddit, tag):
    posts = subreddit.search(tag_str(tag))
    tag_titles = [p.title for p in posts if tag_str(tag) in p.title]

    return tag_titles



def get_tag_info_from_post(tag_title, tag):
    post = next(subreddit.search(tag_title))
    post_info = {
        'user': post.author.name,
        'url': post.url,
        'previous_location': get_location_from_post(post, tag)
    }

    return post_info


def get_location_from_post(post, tag):
    post_content = post.selftext.split('\n')
    location = ''

    for line in post_content:
        if is_old_tag_line(line):
            location = extract_location_from(line, tag)
            break

    return location


def is_old_tag_line(line):
    pattern = r'old|previous|found|tagged'
    match = re.search(pattern, line, re.IGNORECASE)

    return match


def extract_location_from(line, tag):
    old_tag = tag - 1

    patterns_to_remove = [
        rf'\#{old_tag}',
        r'((old|previous)\s)?(bike\s)?((post|tag(ged)?|location)\s)?',
        r'https?\:\/\/(.*?)(\s|\))',
        r'www\.(.*?)(\s|\))',
        r'(location|map(ped|s)?|google)',
        r'(old|previous|found)',
        r'tag(ged)?',
        r'\\',
        r'\:',
        r'\[',
        r'\]',
        r'\)',
        r'\(',
        r'\-',
        r'–',
        r'—',
        r'\!',
        r'^\s*\.'
    ]

    for pattern in patterns_to_remove:
        line = re.sub(pattern, '', line, flags=re.IGNORECASE)

    return line.strip()


def read_manual_override_tags():
    tags = {}

    for file in OVERRIDE_FILES:
        with open(os.path.join(RESOURCE_DIR, file)) as f:
            tag_lines = [json.loads(line) for line in f.readlines()]

        for tag in tag_lines:
            tags[tag['tag']] = {k: v for k,v in tag.items() if k != 'tag'}

    return tags


def has_manual_override(manual_overrides, tag):
    return tag in list(manual_overrides.keys())


def combine_tags(old_tags, new_tags):
    return {**old_tags, **new_tags}


def tag_str(num):
    return f'#{num}'


if __name__ == '__main__':
    parser = parser.parser()
    args = parser.parse_args()

    subreddit = reddit.get_subreddit(SUBREDDIT)

    if args.use_leaderboard:
        current_leaderboard_tags = leaderboard.read_existing_leaderboard_tags(subreddit, PHOTOTAG_WIKI)
        start_tag = leaderboard.last_leaderboard_tag(current_leaderboard_tags)
    else:
        current_leaderboard_tags = {}
        start_tag = DEFAULT_START_TAG

    manual_override_tags = read_manual_override_tags()
    new_tags = get_tags(start_tag, args.current_tag, subreddit, manual_override_tags)
    all_tags = combine_tags(current_leaderboard_tags, new_tags)

    updated_leaderboard = leaderboard.leaderboard(all_tags)
    leaderboard.print_new_leaderboard(updated_leaderboard)
    leaderboard.print_found_tags(all_tags)

    qa.print_report(all_tags, args.current_tag)

