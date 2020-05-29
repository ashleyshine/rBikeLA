def missing_tags(tags, end_tag):
    """Return list of tags missing from tags found in subreddit.

    Params:
        tags: dict
        end_tag: number of last tag (int)
    """
    found_tags = set(tags.keys())
    all_tags = set(range(1, end_tag))

    print(sort(all_tags))
    missing_tags = sort(list(all_tags - found_tags))

    return missing_tags


def total_tags_found(tags):
    return len(tags)


def print_report(tags, end_tag):
    n_tags_found = total_tags_found(tags)
    missing = missing_tags(tags, end_tag)

    print(f'Total tags found: {n_tags_found}')
    print(f'Total missing tags: {len(missing)}')
    print(f'Missing tags: {missing}')
