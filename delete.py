from collections import OrderedDict
from itertools import islice
from pypsnapi import profile, friends
import time
import config

if __name__ == '__main__':
    p = profile.get()
    f = friends.get(p)

    fs = {}
    for friend in f:
        if 'lastOnlineDate' in friend['presence']['primaryInfo']:
            fs[friend['onlineId']] = friend['presence']['primaryInfo']['lastOnlineDate']
        else:
            fs[friend['onlineId']] = friend['presence']['primaryInfo']['onlineStatus']

    print('Current friendlist size: {}'.format(len(fs)))
    if len(fs) > config.cull_to_size:
        sorted_friends = list(islice(OrderedDict(sorted(fs.items(), key=lambda t: t[1])), len(fs) - config.cull_to_size))

        print('Note: this script will delete the following friends from your list: {}'.format(sorted_friends))
        raw_input('Press enter to continue or ctrl-c to cancel...')

        for f in sorted_friends:
            print('Deleting {}...'.format(f))
            friends.delete(f, p)
            time.sleep(1)
    else:
        print('Already have fewer friends than cull_to_size, exiting...')