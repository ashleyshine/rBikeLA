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

1) /u/nigelst 52 tags
2) /u/Howardval 25 tags
3) /u/havetocrow 15 tags
3) /u/cardina16 15 tags
4) /u/flacoloco 14 tags
4) /u/chicago_orgullo 14 tags
4) /u/NeptuNeo 14 tags
5) /u/takeasecond 12 tags
6) /u/Voltairian3 11 tags
7) /u/sdkfhjs 10 tags
7) /u/bergam0t 10 tags
8) /u/soswat 9 tags
9) /u/Jesuspeaksfrench 8 tags
10) /u/dima55 7 tags

# Found tags!

- [Tag #1](http://redd.it/1wshy7) - Koreatown - *found by /u/PizCzar*
- [Tag #2](http://redd.it/1x4yks) - FIDM Downtown - *found by /u/Regret_Nothing*
- [Tag #3](http://redd.it/251t17) - Culver City - *found by /u/Crayz9000*
- [Tag #4](http://redd.it/254u8a) - Venice/Fairfax - *found by /u/underscore*
- [Tag #5](http://redd.it/25f0z4) - Santa Monica City Hall - *found by /u/nigelst*
- [Tag #6](http://redd.it/29c998) - Mulholland Drive Scenic Overlook - *found by /u/somEthingElsEEntirlE*
- [Tag #7](http://redd.it/29e427) - Universal Studios at Lankershim - *found by /u/SwedishChef727*
- [Tag #8](http://redd.it/29faik) - Iliad Book Shop Cahuenga and Chandler - *found by /u/Crayz9000*
- [Tag #9](http://redd.it/29ja1r) - Canter's Deli on Fairfax - *found by /u/somEthingElsEEntirlE*
- [Tag #10](http://redd.it/29sgie) - MacArthur Park Lake - *found by /u/nigelst*
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
