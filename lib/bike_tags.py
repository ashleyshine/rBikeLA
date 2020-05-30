import json
import logging
import os

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

    for n in range(start, end):
        try:
            tags[n] = tag_info(subreddit, n, manual_overrides)
        except Exception as e:
            logging.info(f'Unable to find tag for #{n}. Skipping.')

    return tags


def tag_info(subreddit, tag, manual_overrides={}):
    """Return info for a tag number.
    Params:
        subreddit: praw Subreddit instance
        tag: int
    """
    tag_titles = get_tag_posts(subreddit, tag)
    multiple_posts = has_multiple_posts(tag_titles)
    manual_override = has_manual_override(manual_overrides, tag)

    if multiple_posts and manual_override:
        logging.info(f'More than one post for #{tag}. Using manual override found in resources.')
        post_info = get_tag_info_from_overrides(manual_overrides, tag)
    elif multiple_posts:
        logging.warning(
            f'More than one post found for #{tag}. Skipping. ' +
            'Please resolve manually and add to resource directory.' +
            '\nTag posts: {tag_titles}'
        )
        raise Exception
    else:
        try:
            post_info = get_tag_info_from_post(tag_titles[0])
        except Exception:
            if tag in manual_overrides.keys():
                logging.info(f'Unable to find post for #{tag}. Using manual override found in resources.')
                post_info = get_tag_info_from_overrides(manual_overrides, tag)

    return post_info


def get_tag_posts(subreddit, tag):
    posts = subreddit.search(tag_str(tag))
    tag_titles = [p.title for p in posts if tag_str(tag) in p.title]

    return tag_titles



def get_tag_info_from_post(tag_title):
    post = next(subreddit.search(tag_title))
    post_info = {
        'user': post.author.name,
        'url': post.url
    }

    return post_info


def read_manual_override_tags():
    tags = {}

    for file in OVERRIDE_FILES:
        with open(os.path.join(RESOURCE_DIR, file)) as f:
            tag_lines = [json.loads(line) for line in f.readlines()]

        for tag in tag_lines:
            tags[tag['tag']] = {'user': tag['user'], 'url': tag['url']}

    return tags


def get_tag_info_from_overrides(manual_overrides, tag):
    tag_info = {
        'user': manual_overrides[tag]['user'],
        'url': manual_overrides[tag]['url']
    }

    return tag_info


def has_multiple_posts(tag_titles):
    return len(tag_titles) > 1


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
    leaderboard.print_new_leaderboard(updated_leaderboard, 15)
    leaderboard.print_found_tags(all_tags)

    qa.print_report(all_tags, args.current_tag)
