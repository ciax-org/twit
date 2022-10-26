#!/usr/bin/python


import getopt
import sys
import tweepy
# Version used 4.10.1

# Import credentials from a python file containing your credentials, or comment this import out
'''
import credentials as cr
consumer_key = cr.consumer_key
consumer_secret = cr.consumer_secret
access_token = cr.access_token
access_token_secret = cr.access_token_secret
'''

import json
# or have credentials loaded from a 'secure' config.json file at runtime. Create the file using the json below;
'''
{
    "consumer_key": "FILL", 
    "consumer_secret": "FILL",
    "access_token": "FILL",
    "access_token_secret": "FILL"
}
'''

runtime_credentials_load = True

# or set them below (not recommended for 'security')

using_credentials_import = True

if not using_credentials_import:

    # Copy these lines and paste in credentials.py or set them here
    consumer_key = '<FILL>'
    consumer_secret = '<FILL>'
    access_token = '<FILL>'
    access_token_secret = '<FILL>'


def nicely_exit(msg):

    print(msg)
    exit(0)


def init():

    if runtime_credentials_load:

        try:

            with open(r'config.json', 'rb') as f:

                d = json.load(f)

                for k, v in d.items():

                    # This is beautifully lazy, but not ideal 'security' as it creates variables from the json file
                    globals()[k] = v

                # Alternative
                '''
                consumer_key = d['consumer_key']
                consumer_secret = d['consumer_secret']
                access_token = d['access_token']
                access_token_secret = d['access_token_secret']
                '''

        except FileNotFoundError:

            nicely_exit('File does not exist')


def process_friend(api, friend):

    users = api.lookup_users(user_id=[friend])

    # Only [1 user], but this pattern works for [1, or many]
    for user in users:

        return user.screen_name, not user.notifications


def set_notifications(user_id, notifications):

    init()

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True)

    ids = api.get_friend_ids(user_id=user_id)

    updated_cnt = 0
    friend_cnt = 0

    for friend_id in ids:

        friend_cnt += 1

        screen_name, needs_updating = process_friend(api, friend_id)
        print(screen_name, end='')

        if needs_updating:

            api.update_friendship(user_id=friend_id, device=notifications)
            print(' ', 'Enabled notifications', end='')
            updated_cnt += 1

        print('')

    print(f'Of {friend_cnt} friends {updated_cnt} updated')


def print_help():

    print('Set notifications of tweets from all friends of user with <id or screen_name> to -yes or -no.')
    print('main.py -id <id or screen_name> -yes | -no')


def main(argv):

    user_id = None
    notifications = None

    try:

        opts, args = getopt.getopt(argv, 'hi:yn', ['help', 'id=', 'yes', 'no'])

    except getopt.GetoptError:
        print_help()
        sys.exit(2)

    for opt, arg in opts:

        if opt == '-h':
            print_help()
            sys.exit()
        elif opt in ('-i', '--id'):
            user_id = arg
        elif opt in ('-y', '--yes'):
            notifications = True
        elif opt in ('-n', '--no'):
            notifications = False

    print('user_id ', user_id)
    print('notifications ', notifications)

    if user_id and notifications is not None:
        print('Processing ')
        set_notifications(user_id, notifications)
    else:
        print_help()


if __name__ == "__main__":

    main(sys.argv[1:])
