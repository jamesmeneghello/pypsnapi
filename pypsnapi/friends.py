import urllib
import json

import pypsnapi.auth
import pypsnapi.profile

FRIENDS_URL = 'https://{}-prof.np.community.playstation.net:443/userProfile/v1/users/{}/friendList{}'


def get(profile=None):
    auth = pypsnapi.auth.auth()

    if not profile:
        profile = pypsnapi.profile.get()

    payload = {
        'fields': 'onlineId',
        'sort': 'onlineId',
        'friendStatus': 'friend',
        'presenceType': 'primary',
        'avatarSize': 'm',
        'limit': '1',
        'offset': '0'
    }

    f = auth.get(FRIENDS_URL.format(profile['region'], profile['onlineId'], '?' + urllib.urlencode(payload)))
    friend_data = json.loads(f.text)

    limit = 50
    payload['limit'] = limit
    offset = 0
    total = friend_data['totalResults']
    friends = []
    while offset < total:
        payload['offset'] = offset
        f = auth.get(FRIENDS_URL.format(profile['region'], profile['onlineId'], '?' + urllib.urlencode(payload)))
        friend_data = json.loads(f.text)
        friends += friend_data['friendList']

        offset += limit

    return friends


def delete(online_id, profile=None):
    auth = pypsnapi.auth.auth()

    if not profile:
        profile = pypsnapi.profile.get()

    print(auth.delete(FRIENDS_URL.format(profile['region'], profile['onlineId'], '/' + online_id)))