# When did BTS broke last?

Homepage: https://bts.cupco.de

## Install

For contributing:

1.  Create a virtualenv (optional)
2.  `pip install -r requirements-dev.txt`
3.  `pre-commit install`
4.  Follow the next steps

Running:

1.  Set `TWITTER_CONSUMER_KEY`, `TWITTER_CONSUMER_SECRET`, `TWITTER_ACCESS_TOKEN`, `TWITTER_ACCESS_TOKEN_SECRET` (get them from https://apps.twitter.com/)
2.  Run `python manage.py migrate` to setup database
3.  Run `python manage.py createsuperuser` to create admin user

## Commands

Run these with `python manage.py`

* `runserver`: Start the development web server
* `fetch_tweet`: Update tweet database
* `bts_tweet_analysis`: Perform analysis on stored tweets
