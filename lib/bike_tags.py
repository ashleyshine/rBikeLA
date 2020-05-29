import re
import logging

import reddit
import leaderboard
import parser
import qa

logging.getLogger().setLevel(logging.INFO)


SUBREDDIT = 'bikeLA'
PHOTOTAG_WIKI = 'phototag'
DEFAULT_START_TAG = 1
END_TAG = 388


def get_tags(start, end, subreddit):
    """Return dict in format {tag: tag_info}.

    Params:
        start: tag number (int)
        end: tag number (int)
        subreddit: praw Subreddit instance
    """
    tags = {}

    for n in range(start, end):
        try:
            tags[n] = tag_info(subreddit, n)
        except Exception as e:
            logging.info(f'Unable to find tag for #{n}. Skipping.')

    return tags


def tag_info(subreddit, tag):
    """Return info for a tag number.
    Params:
        subreddit: praw Subreddit instance
        tag: int
    """
    posts = subreddit.search(tag_str(tag))
    tag_title = [p.title for p in posts if tag_str(tag) in p.title]

    if len(tag_title) > 1:
        logging.warning(f'More than one tag post found for {tag}. Skipping. Please resolve manually.')
        logging.warning(f'Tag posts: {tag_title}')
        raise Exception
    else:
        post = next(subreddit.search(tag_title))
        post_info = {
            'user': post.author.name,
            'url': post.permalink
        }

    return post_info


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

    new_tags = get_tags(start_tag, args.current_tag, subreddit)
    all_tags = combine_tags(current_leaderboard_tags, new_tags)

    updated_leaderboard = leaderboard.leaderboard(all_tags)
    sorted_leaderboard = leaderboard.sort_leaderboard(updated_leaderboard)

    n_tags_found = qa.total_tags_found(all_tags)
    missing = qa.missing_tags(all_tags, END_TAG)

    # TODO: get tag urls


