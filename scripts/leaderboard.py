import collections
import re


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
            tag = int(tag_line.group(1))
            url = tag_line.group(2)
            location = tag_line.group(4)
            found_by = tag_line.group(6)
            user = tags[tag-1]['found_by'] if tag != 1 else ''

            tags[tag] = {
                'location': location,
                'url': url,
                'found_by': found_by,
                'user': user
            }

    return tags


def match_tag_line(line):
    """Return re Match object if the line contains a tag.

    Params:
        line: str
    """
    pattern = r'\[Tag #(\d+)\]\((http.*)\)( - )?(.*)( - )\*found by /u/(.*)\*'
    match = re.search(pattern, line, re.IGNORECASE)
    return match


def leaderboard(tags):
    """Return dict in form of {user: num_tags}.

    Params:
        tags: dict
    """
    leaderboard = collections.defaultdict(int)

    users = [tag_info['user'] for tag_info in tags.values()]

    for user in users:
        leaderboard[user] += 1

    leaderboard_with_users_combined = combine_identical_users(leaderboard)

    return leaderboard_with_users_combined


def sort_leaderboard(leaderboard):
    """Return leaderboard as list sorted in descending order of num_tags.

    Params:
        leaderboard: dict in form of {user: num_tags}
    """
    sorted_leaderboard = [
        {user: num_tags} for user, num_tags
        in sorted(leaderboard.items(), key=lambda item: item[1], reverse=True)
    ]

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
    users_with_multiple_names = [
        user for user, count
        in collections.Counter(lowercase_users).items() if count > 1
    ]

    return users_with_multiple_names


def all_user_names(leaderboard, user):
    """Return list of all the usernames that appear for a given user
        in the leaderboard.

    Params:
        leaderboard: dict in form of {user: num_tags}
        user: str
    """
    return [u for u in leaderboard.keys() if u.lower() == user.lower()]


def name_to_keep(all_user_names, user):
    """Return the username to keep for a user whose name appears multiple times.
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


def print_new_leaderboard(leaderboard, top_n):
    """Print top N leaderboard by number of tags found.

    Params:
        leaderboard: dict in form of {user: num_tags}
        top_n: int
    """
    rank = 0
    nth_user = 0
    current_num_tags = float('inf')

    sorted_leaderboard = sort_leaderboard(leaderboard)

    print('# TAG LEADERBOARD\n')

    while rank < top_n and nth_user < len(sorted_leaderboard):
        user, n_tags = list(sorted_leaderboard[nth_user].items())[0]

        if current_num_tags > n_tags:
            current_num_tags = n_tags
            rank += 1

        print(format_leaderboard_line(rank, user, n_tags))

        nth_user += 1


def format_leaderboard_line(rank, user, n_tags):
    return f'{rank}) /u/{user} {n_tags} tags'


def print_found_tags(tags):
    """Print list of found tags.

    Params:
        tags: dict
    """
    tag_numbers = sorted(tags.keys())

    print('\n# Found tags!\n')

    for n in tag_numbers[:-1]:
        url = tags[n]['url']
        location = tags[n]['location']
        found_by = tags[n+1]['user']

        print(format_found_tag_line(n, url, location, found_by))


def format_found_tag_line(n, url, location, found_by):
    formatted_tag = f'[Tag #{n}]({url})'
    formatted_location = f' - {location} - ' if location else ' - '
    formatted_user = f'*found by /u/{found_by}*'

    line = f'- {formatted_tag}{formatted_location}{formatted_user}'

    return line