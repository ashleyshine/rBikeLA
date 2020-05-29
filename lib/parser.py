import argparse

def parser():
    parser = argparse.ArgumentParser(description="Update r/bikeLA bike tag leaderboard.")

    parser.add_argument(
        '--current_tag', '-c', help='Current tag in r/bikeLA',
        type=int, required=True
    )
    parser.add_argument(
        '--use_leaderboard', '-u',
        help='Read tags from leaderboard. If False, start processing posts from Tag #1.',
        type=bool, required=False, default=True
    )

    return parser
