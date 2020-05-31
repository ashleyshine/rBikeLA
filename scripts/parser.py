import argparse


def parser():
    parser = argparse.ArgumentParser(
        description="Get updated r/bikeLA bike tag leaderboard."
    )
    parser.add_argument(
        '--current_tag', '-c', help='Current tag in r/bikeLA',
        type=int, required=True
    )
    parser.add_argument(
        '--n_leaderboard', '-n', help='Length of leaderboard to output (top N by rank)',
        type=int, required=False, default=10
    )
    parser.add_argument(
        '--use_wiki', '-u',
        help='Read tags from wiki. If False, start processing posts from Tag #1',
        type=bool, required=False, default=True
    )
    parser.add_argument(
        '--qa', '-q', help='Print QA report',
        type=bool, required=False, default=False
    )

    return parser
