# rBikeLA

Scripts to get an updated [bike tag](https://www.reddit.com/r/BikeLA/wiki/phototag) leaderboard and found tags list from [/r/bikeLA](https://www.reddit.com/r/BikeLA).

## Installation
You will need **Python 3** installed.

Clone this repo:
```
git clone git@github.com:ashleyshine/rBikeLA.git
cd rBikeLA
```

If you want to use a virtual environment (recommended):
```
pip3 install -U pip
python3 -m venv rbikela_env
source rbikela_env/bin/activate
```

Install required packages:
```
pip3 install -r requirements.txt
```

### Adding a Reddit Developer Token
In order to interface with reddit using its [API](https://www.reddit.com/dev/api), you will need to authenticate with OAuth2. Follow the this [quick start example](https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps) to create an app. You will need your client ID and secret.

Once you've created an app, create a `config/` directory and add your client ID, client secret, and user agent (reddit username) in JSON format to a file called `client` in the directory.
```
mkdir config
cd config
touch client
```
The contents of the `client` file should look like:
```
{"client_id": "<CLIENT_ID>", "client_secret": "<CLIENT_SECRET>", "user_agent": "<USERNAME>"}
```

## Usage
To generate the bike tag leaderboard, call the `get_leaderboard.py` script. There are a few options you can configure.
```
~/Projects/rBikeLA (master) ❯ python3 ./scripts/get_leaderboard.py --help
usage: get_leaderboard.py [-h] --current_tag CURRENT_TAG
                          [--n_leaderboard N_LEADERBOARD]
                          [--use_wiki USE_WIKI] [--qa QA]

Get updated r/bikeLA bike tag leaderboard.

optional arguments:
  -h, --help            show this help message and exit
  --current_tag CURRENT_TAG, -c CURRENT_TAG
                        Current tag in r/bikeLA
  --n_leaderboard N_LEADERBOARD, -n N_LEADERBOARD
                        Length of leaderboard to output (top N by rank)
  --use_wiki USE_WIKI, -u USE_WIKI
                        Read tags from wiki. If False, start processing posts
                        from Tag #1
  --qa QA, -q QA        Print QA report
```

By default, tags already listed on the leaderboard wiki will be used unless `--use_wiki False` is passed.

### Example
The following call will print an updated leaderboard and found tags list up to tag #392. The leaderboard and found tags list are formatted in Markdown, so they can be directly copy & pasted into the phototag wiki.
```
./scripts/get_leaderboard.py -c 392 -q True
```
Example output:
```
# TAG LEADERBOARD

Rank | User| Tags
---|---|---
1 | /u/nigelst | 55
2 | /u/sdkfhjs | 31
3 | /u/havetocrow | 29
4 | /u/tangyline | 27
5 | /u/Howardval | 25
5 | /u/faihube | 25
6 | /u/Wu_Tang_In_a_Pouch | 23
7 | /u/Not_that_easy | 22
8 | /u/chicago_orgullo | 20
9 | /u/takeasecond | 19
10 | /u/coonster | 18

# Found tags!

| Tag | Location | GPS | Found By |
| --- | --- | --- | --- |
| [#1](https://www.reddit.com/r/BikeLA/comments/1wshy7/photo_tag_adapting_from_rbikingatx/) | Koreatown | (34.06119, -118.307197) | /u/PizCzar* |
| [#2](https://www.reddit.com/r/BikeLA/comments/1x4yks/photo_tag_2/) | FIDM Downtown | (34.04406, -118.25976) | /u/Regret_Nothing* |
| [#3](https://www.reddit.com/r/BikeLA/comments/251t17/bike_tag_3/) | Culver City | (34.030418, -118.372549) | /u/Crayz9000* |
| [#4](https://www.reddit.com/r/BikeLA/comments/254u8a/bike_tag_4/) | Venice/Fairfax | (34.039183, -118.370637) | /u/underscore* |
| [#5](https://www.reddit.com/r/BikeLA/comments/25f0z4/bike_tag_5/) | Santa Monica City Hall | (34.011638, -118.491688) | /u/nigelst* |
| [#6](https://www.reddit.com/r/BikeLA/comments/29c998/bike_tag_6/) | Mulholland Drive Scenic Overlook | (34.131533, -118.433612) | /u/somEthingElsEEntirlE* |
| [#7](https://www.reddit.com/r/BikeLA/comments/29e427/bike_tag_7/) | Universal Studios at Lankershim | (34.138875, -118.362376) | /u/SwedishChef727* |
| [#8](https://www.reddit.com/r/BikeLA/comments/29faik/bike_tag_8/) | Iliad Book Shop Cahuenga and Chandler | (34.168645, -118.361667) | /u/Crayz9000* |
| [#9](https://www.reddit.com/r/BikeLA/comments/29ja1r/bike_tag_9/) | Canter's Deli on Fairfax | (34.078985, -118.361368) | /u/somEthingElsEEntirlE* |
| [#10](https://www.reddit.com/r/BikeLA/comments/29sgie/bike_tag_10/) | MacArthur Park Lake | (34.058184, -118.279101) | /u/nigelst* |
```
It will also print a QA report, which can be used to check for missing tags.
```
===== QA Report =====
Total tags found: 392
Total missing tags: 0
Missing tags: []
```

### Manual Overrides
If multiple posts are found for a bike tag or no post is found for a bike tag, you will see messages like this:
```
WARNING: No posts found for #290. Skipping.Please find post manually and add to resource directory.

WARNING: More than one post found for #341. Skipping. Please resolve manually and add to resource directory.
Tag posts: ['Bike Tag #341', 'Bike Tag #341']
```
You can manually look up the tag post in [/r/bikeLA](https://www.reddit.com/r/BikeLA/) and add them to the `resources` directory in JSON format, with one tag per line. If a manual override exists for a tag, it will always be preferred when retrieving new tag info.
