import datetime
from datetime import timezone
import praw
from pymongo import MongoClient
import sys
import traceback

# Reddit client configuration:
BOT_USERNAME = 'BOT_USERNAME'
BOT_PASSWORD = 'BOT_PASSWORD'
BOT_CLIENT_ID = 'BOT_CLIENT_ID'
BOT_CLIENT_SECRET = 'BOT_CLIENT_SECRET'
BOT_USER_AGENT = 'BOT_USER_AGENT'

# Subreddit/database configuration:
SUBREDDIT = 'SUBREDDIT'
MONGO_DB = 'MONGO_DB'

# Delete records older than the following:
YEARS = 0
MONTHS = 2
DAYS = 0


class Bot():
    def __init__(self):
        self.reddit = praw.Reddit(username=BOT_USERNAME,
                                  password=BOT_PASSWORD,
                                  client_id=BOT_CLIENT_ID,
                                  client_secret=BOT_CLIENT_SECRET,
                                  user_agent=BOT_USER_AGENT)
        self.set_ttl_index()

    def botcode(self):
        for submission in self.reddit.subreddit(SUBREDDIT).stream.submissions(skip_existing=True):
            if submission.is_self:
                continue

            db_client = MongoClient(MONGO_DB)
            links = db_client.namethatsong.links
            duplicate_result = self.check_submission_for_duplicates(submission)
            if duplicate_result == None:
                record = {
                    'submission_url': submission.url,
                    'submission_title': submission.title,
                    'submission_id': submission.id,
                    'expire_at': datetime.datetime.utcnow(),
                    'posted_at': submission.created_utc
                }
                links.insert_one(record)
            else:
                last_submission_date = datetime.datetime.fromtimestamp(
                    duplicate_result['posted_at'])
                repost_link = self.reddit.submission(
                    duplicate_result['submission_id']).permalink
                formatted_date = last_submission_date.strftime('%Y-%m-%d')
                submission.report('Possible repost from {}. Link: {}'.format(
                    formatted_date, repost_link))

    def set_ttl_index(self):
        db_client = MongoClient(MONGO_DB)
        links = db_client.namethatsong.links
        links.create_index(
            'expire_at', expireAfterSeconds=self.calculate_expiration())

    def check_submission_for_duplicates(self, submission):
        db_client = MongoClient(MONGO_DB)
        links = db_client.namethatsong.links

        return links.find_one({'submission_url': submission.url})

    def calculate_expiration(self):
        days = (YEARS * 12 * 30) + (MONTHS * 30) + DAYS
        seconds = days * 24 * 60 * 60

        return seconds


if __name__ == '__main__':
    try:
        Bot().botcode()
    except KeyboardInterrupt:
        sys.exit(0)
    except Exception:
        traceback.print_exc()
