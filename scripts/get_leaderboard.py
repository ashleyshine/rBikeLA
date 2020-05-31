import bike_tags
import reddit
import leaderboard
import parser
import qa

SUBREDDIT = 'bikeLA'
PHOTOTAG_WIKI = 'phototag'
RESOURCE_DIR = './resources'
OVERRIDE_FILES = ['conflicting_tags.json', 'missing_tags.json']
DEFAULT_START_TAG = 1


if __name__ == '__main__':
    parser = parser.parser()
    args = parser.parse_args()

    subreddit = reddit.get_subreddit(SUBREDDIT)

    if args.use_wiki:
        current_leaderboard_tags = leaderboard.read_existing_leaderboard_tags(subreddit, PHOTOTAG_WIKI)
        start_tag = leaderboard.last_leaderboard_tag(current_leaderboard_tags)
    else:
        current_leaderboard_tags = {}
        start_tag = DEFAULT_START_TAG

    manual_override_tags = bike_tags.read_manual_override_tags(RESOURCE_DIR, OVERRIDE_FILES)
    new_tags = bike_tags.get_tags(start_tag, args.current_tag, subreddit, manual_override_tags)
    all_tags = bike_tags.combine_tags(current_leaderboard_tags, new_tags)

    updated_leaderboard = leaderboard.leaderboard(all_tags)
    leaderboard.print_new_leaderboard(updated_leaderboard, args.n_leaderboard)
    leaderboard.print_found_tags(all_tags)

    if args.qa:
        qa.print_report(all_tags, args.current_tag)
