reddit-resub
============

Export / import subreddits from a Reddit account.

Useful when you create a new user account, or if you want to drop the default subreddit subscriptions or maybe you only read /r/IAmA on a Thursday but read all the /r/Ask* subreddits on Saturday.

Usage Instructions
============

    usage: resub.py [-h] [--import] [--user USER] [--file FILE]

    Resubscribe to your old subreddits.

    optional arguments:
      -h, --help            show this help message and exit
      --import, -i          Specify -i to import to the user Default is to save
                        from a user (safe).
      --user USER, -u USER  Reddit username.
      --file FILE, -f FILE  Provide a filename to use.

Example Usage
============
* Save user x89's subreddits to file abc.subs

    `python resub.py --user x89 --file abc.subs`    

* Import the subreddits listed in abc.subs to user x78

    `python resub.py --import --user x78 --file abc.subs`    

* Set up environment
```
 git clone https://github.com/x89/reddit-resub
 cd reddit-resub
 virtualenv . -p python3
 source bin/activate
 pip install -r requirements.txt
```
