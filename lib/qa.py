def missing_tags(tags, end_tag):
    """Return list of tags missing from tags found in subreddit.

    Params:
        tags: dict in form of {tag: user}
        end_tag: number of last tag (int)
    """
    found_tags = set(tags.keys())
    all_tags = set(range(1, end_tag))
    missing_tags = list(all_tags - found_tags)

    return missing_tags


def total_tags_found(all_tags):
    return len(all_tags)

