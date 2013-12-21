import json

import pypsnapi.auth

PROFILE_URL = 'https://vl.api.np.km.playstation.net/vl/api/v1/mobile/users/me/info'


def get():
    auth = pypsnapi.auth.auth()
    profile = auth.get(PROFILE_URL)
    return json.loads(profile.text)
