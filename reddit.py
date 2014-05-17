#!/usr/bin/env python3

import praw
import argparse
import json
from time import sleep

parser = argparse.ArgumentParser(description='Resubscribe to your old subreddits.')
parser.add_argument('--import', '-i', action="store_true", help="Specify -i to import to the user\
        Default is to save from a user (safe).")
parser.add_argument('--user', '-u', help="Reddit username.")
parser.add_argument('--file', '-f', help="Provide a filename to use.")

class Resub:
    _r = praw.Reddit('reddit-resub')
    _reddit_sleep = 2 #  Seconds to sleep for, Reddit requests you don't do more than 2 per second.
    _default_subreddits = (
        'announcements',
        'art',
        'askreddit',
        'askscience',
        'aww',
        'blog',
        'books',
        'creepy',
        'dataisbeautiful',
        'diy',
        'documentaries',
        'earthporn',
        'explainlikeimfive',
        'fitness',
        'food',
        'funny',
        'futurology',
        'gadgets',
        'gaming',
        'getmotivated',
        'gifs',
        'history',
        'iama',
        'internetIsBeautiful',
        'jokes',
        'lifeprotips',
        'listentothis',
        'mildlyinteresting',
        'movies',
        'music',
        'news',
        'nosleep',
        'nottheonion',
        'oldschoolcool',
        'personalfinance',
        'philosophy',
        'photoshopbattles',
        'pics',
        'science',
        'showerthoughts',
        'space',
        'sports',
        'television',
        'tifu',
        'todayilearned',
        'twoXChromosomes',
        'upliftingnews',
        'videos',
        'worldnews',
        'writingprompts',
    )

    def __init__(self, subscribe, user=None, filename=None):
        self._r.login(user)
        self._user = self.get_user()

        if not filename:
            filename = '{user}.subs'.format(user=self._user)
        self._filename = filename

        if subscribe:
            print("Subscribing to subreddits in '{file}'".format(file=filename, user=self.get_user()))
            self.import_subs()
        else:
            print("Exporting {user}'s subreddits to {file}".format(file=filename, user=self.get_user()))
            self.export_subs()

    def unsub_defaults(self):
        '''
        Unsubscribes from all default subreddits.
        '''
        print("Unsubscribing from all default subreddits")
        for sub in self._default_subreddits:
            self._r.unsubscribe(sub)
            print("Unsubscribed from default subreddit {sub}".format(sub=sub))
            sleep(self._reddit_sleep)

    def import_subs(self):
        '''
        Uses subreddits defined in JSON format in a file to import to a Reddit
        user account. Unsubscribes from default subreddits first.
        '''
        fh = open(self._filename, 'r')
        new_subs = json.load(fh)
        fh.close()
        self.unsub_defaults()
        my_subs = list(
            set(self.get_subs()) - (set(self._default_subreddits) | set(new_subs))
        )
        for sub in my_subs:
            self._r.unsubscribe(sub)
            print("Unsubscribed from subreddit {sub}".format(sub=sub))
            sleep(self._reddit_sleep)
        for sub in new_subs:
            if sub not in my_subs:
                self._r.subscribe(sub)
                print("Subscribed to {sub}".format(sub=sub))
                sleep(self._reddit_sleep)

    def get_user(self):
        '''
        Specifically returns the username from the Reddit object, not the one
        specified by the user / script. This is guaranteed to be correct in 
        other words.
        '''
        return str(self._r.user)

    def export_subs(self):
        '''
        Saves the user's subreddits to file.
        '''
        fh = open(self._filename, 'w')
        json.dump(self.get_subs(), fh)
        fh.close()

    def get_subs(self):
        '''
        Returns a unique list of subreddits to which the user is subscribed.
        '''
        my_subs = set()
        for sub in self._r.get_my_subreddits(limit=None):
            my_subs.add(str(sub))
        return list(my_subs)


if __name__ == "__main__":
    args = parser.parse_args()

    # Boolean, True if --import / -i
    # If true then subscribe, if false then export to file.
    subscribe = getattr(args, 'import')

    r = Resub(subscribe, filename=getattr(args, 'file'), user=getattr(args, 'user'))
