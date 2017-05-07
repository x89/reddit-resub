#!/usr/bin/env python3

import praw
import argparse
import json

parser = argparse.ArgumentParser(description='Resubscribe to your old subreddits.')
parser.add_argument('--import', '-i', action="store_true", help="Specify -i to import to the user\
        Default is to save from a user (safe).")
parser.add_argument('--user', '-u', help="Reddit username.")
parser.add_argument('--file', '-f', help="Provide a filename to use.")

class Resub:
    _r = praw.Reddit('reddit-resub 2016-02-20')
    _default_subreddits = (
        'announcements', 'art', 'askreddit', 'askscience', 'aww', 'blog',
        'books', 'creepy', 'dataisbeautiful', 'diy', 'documentaries',
        'earthporn', 'explainlikeimfive', 'fitness', 'food', 'funny',
        'futurology', 'gadgets', 'gaming', 'getmotivated', 'gifs', 'history',
        'iama', 'internetIsBeautiful', 'jokes', 'lifeprotips', 'listentothis',
        'mildlyinteresting', 'movies', 'music', 'news', 'nosleep',
        'nottheonion', 'oldschoolcool', 'personalfinance', 'philosophy',
        'photoshopbattles', 'pics', 'science', 'showerthoughts', 'space',
        'sports', 'television', 'tifu', 'todayilearned', 'twoXChromosomes',
        'upliftingnews', 'videos', 'worldnews', 'writingprompts',
    )

    def __init__(self, subscribe, user=None, filename=None):
        self._r.login(user)
        self._user = self.get_user()

        if not filename:
            filename = '{user}.subs'.format(user=self._user)
        self._filename = filename

        if subscribe:
            print("Subscribing to subreddits in '{file}'".format(file=filename, user=self.get_user()))
            self.sub_clever()
        else:
            print("Exporting {user}'s subreddits to {file}".format(file=filename, user=self.get_user()))
            self.export_subs()

    def unsub(self, subreddit):
        '''
        Unsubscribes and prints to STDOUT
        '''
        try:
            self._r.unsubscribe(subreddit)
            print("Unsubscribed from subreddit {sub}".format(sub=subreddit))
        except praw.errors.NotFound:
            print("Not subscribed to %s, skipping" % sub)

    def sub(self, subreddit):
        '''
        Try to subscribe to a given subreddit.
        '''
        try:
            self._r.subscribe(subreddit)
            print("Subscribed to {sub}".format(sub=subreddit))
        except praw.errors.Forbidden:
            print("Subreddit %s is private, skipping." % subreddit)

    def unsub_all(self):
        '''
        Unsubscribes from every subreddit.
        '''
        for subreddit in self.get_subs():
            self.unsub(subreddit)

    def unsub_defaults(self):
        '''
        Unsubscribes from all default subreddits.
        Basically depricated because we'll unsubscribe from
        everything 
        '''
        print("Unsubscribing from all default subreddits")
        for sub in self._default_subreddits:
            self.unsub(sub)

    def get_wanted_subs(self):
        '''
        Opens the list of subreddits we want to subscribe to
        from a json fille.
        '''
        fh = open(self._filename, 'r')
        subs = json.load(fh)
        fh.close()
        return list(set(subs))

    def sub_clever(self):
        '''
        Tries to be clever.
        '''
        wanted_subs = self.get_wanted_subs()
        current_subs = self.get_subs()
        magic = set(wanted_subs) - set(current_subs)
        for sub in magic:
            if sub in wanted_subs:
                self.sub(sub)
            elif sub not in wanted_subs:
                self.unsub(sub)

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
        json.dump(sorted(self.get_subs()), fh, indent=2)
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
