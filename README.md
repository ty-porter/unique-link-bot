# NameThatSongBot
Stores potential reposts in a MongoDB database and reports any new posts if they have been posted within a configurable amount of time.

### Configuration
Before running the bot, you'll need to add your credentials to `bot.py`

#### Reddit client configuration:
```
BOT_USERNAME = 'BOT_USERNAME'
BOT_PASSWORD = 'BOT_PASSWORD'
BOT_CLIENT_ID = 'BOT_CLIENT_ID'
BOT_CLIENT_SECRET = 'BOT_CLIENT_SECRET'
BOT_USER_AGENT = 'BOT_USER_AGENT'
```

* `BOT_USERNAME` and `BOT_PASSWORD` are the credentials for your bot's Reddit account
* `BOT_CLIENT_ID` and `BOT_CLIENT_SECRET` can be found in [your preferences](https://www.reddit.com/prefs/apps)
* `BOT_USER_AGENT` is required to identify your bot to Reddit -- a good example would be `NameThatSongBot 1.0 by /u/pawptart "https://github.com/pawptart/unique-link-bot"`

#### Subreddit/database configuration:
```
SUBREDDIT = 'SUBREDDIT'
MONGO_DB = 'MONGO_DB'
```

* `SUBREDDIT` is the subreddit you intend to run this bot on
* `MONGO_DB` is your MongoDB connection string

#### Delete records older than the following:
```
YEARS = 0
MONTHS = 2
DAYS = 0
```

Use these fields to set how long to limit reposts for a particular link.

### Usage

Download `bot.py`, navigate to a terminal and run `python bot.py`, and you're good to go. Follow instructions [here](https://www.reddit.com/r/RequestABot/comments/cyll80/a_comprehensive_guide_to_running_your_reddit_bot/) for in-depth setup of Python on your machine if required.
