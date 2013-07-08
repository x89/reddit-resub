#!/usr/bin/env python2
import praw, argparse, json

parser = argparse.ArgumentParser(description='Resubscribe to your old subreddits.')
parser.add_argument('--import', '-i', action="store_true")
parser.add_argument('--user', '-u', help="Reddit username to import from/to.")
parser.add_argument('--file', '-f', help="Provide a filename to export to / import from.")
parser.add_argument('--debug', '-d', action="store_true")

class Resub:
    r = praw.Reddit('reddit-resub')
    user = None
    file = None
    debug = False
    default_subreddits = (
        'AdviceAnimals',
        'AskReddit',
        'IAmA',
        'WTF',
        'announcements',
        'atheism',
        'aww',
        'bestof',
        'blog',
        'funny',
        'gaming',
        'movies',
        'music',
        'news',
        'pics',
        'politics',
        'science',
        'technology',
        'todayilearned',
        'videos',
        'worldnews'
    )

    def __init__(self):
        args = parser.parse_args()
        self.debug = args.debug
        self.user = args.user
        self.r.login(self.user)

        if args.file:
            self.file = args.file
        else:
            self.file = '{0}.subs'.format(self.get_user())

        if self.debug:
            print "Using file: {0}".format(self.file)

        if args.__dict__['import']:
            if self.debug:
                print "Importing subreddits to user {0}...".format(self.get_user())
            self.import_subs()
        else:
            if self.debug:
                print "Exporting {0}'s subreddits...".format(self.get_user())
            self.export_subs()

    def import_subs(self):
        new_subs = []
        with open(self.file, 'r') as fh:
            new_subs = json.load(fh)
        for sub in self.default_subreddits:
            self.r.unsubscribe(sub)
        for sub in new_subs:
            self.r.subscribe(sub)
        return True

    def get_user(self):
        return self.r.user.__unicode__()

    def export_subs(self):
        subs = json.dumps(self.get_subs())
        with open(self.file, 'w') as fh:
            fh.write(subs)

    def get_subs(self):
        my_subs = set()
        for sub in self.r.get_my_subreddits():
            my_subs.add(sub.__unicode__())
        return list(set(my_subs))

if __name__ == "__main__":
    Resub()
