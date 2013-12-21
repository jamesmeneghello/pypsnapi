import mechanize
import cookielib
import re
import requests
import json
import datetime

import config

from pypsnapi import log
from requests_oauthlib import OAuth2Session

SCOPE = 'sceapp'
REDIRECT_URL = 'com.scee.psxandroid.scecompcall://redirect'

CONSUMER_KEY = 'b0d0d7ad-bb99-4ab1-b25e-afa0c76577b0'
CONSUMER_SECRET = 'Zo4y8eGIa3oazIEp'

FORM_URL = 'https://reg.api.km.playstation.net:443/regcam/mobile/sign-in.html'
OAUTH_URL = 'https://auth.api.sonyentertainmentnetwork.com/2.0/oauth/token'


def setup(browser):
    cj = cookielib.LWPCookieJar()
    browser.set_cookiejar(cj)
    browser.set_handle_equiv(True)
    browser.set_handle_gzip(True)
    browser.set_handle_redirect(True)
    browser.set_handle_referer(True)
    browser.set_handle_robots(False)
    browser.set_handle_refresh(mechanize.HTTPRefreshProcessor(), max_time=1)

    # nexus 5 user-agent
    browser.addheaders = [('User-agent', 'Mozilla/5.0 (Linux; Android 4.4.2; Nexus 5 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.59 Mobile Safari/537.36')]


def auth():
    oauth_data = _auth()
    if oauth_data:
        return OAuth2Session(CONSUMER_KEY, token=oauth_data)
    else:
        return None


def _auth():
    try:
        with open('.oauth', 'r') as oauth_file:
            data = json.load(oauth_file)
            if datetime.datetime.strptime(data['date'], '%Y-%m-%dT%H:%M:%S.%f') + datetime.timedelta(seconds=data['expires_in']) < datetime.datetime.now():
                return refresh(data['refresh_token'])
            else:
                return data
    except IOError:
        return login(config.email, config.password)


def login(email, password):
    br = mechanize.Browser()
    setup(br)

    resp = br.open(FORM_URL)
    log.debug(resp.read())

    # select the sign-in form
    br.select_form(nr=0)
    br.form.set_all_readonly(False)

    # fill details
    br['email'] = email
    br['password'] = password
    br['client_id'] = CONSUMER_KEY
    br['scope'] = SCOPE
    br['redirectURL'] = REDIRECT_URL

    # submit the form and grab the response
    resp = br.submit().read()
    log.debug(resp)

    result = re.search('authCode=(.*)\';', resp)
    if result:
        auth_code = result.group(1)
    else:
        log.error('Problem with sign-in page.')
        return False

    payload = {
        'grant_type': 'authorization_code',
        'client_id': CONSUMER_KEY,
        'client_secret': CONSUMER_SECRET,
        'code': auth_code,
        'redirect_uri': REDIRECT_URL,
        'state': 'x',
        'scope': 'psn:' + SCOPE,
        'duid': '0000000d00040080E0255A3843F84F5AAAA71D85EDB98F37'
    }

    return send_oauth(payload)


def refresh(refresh_token):
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': refresh_token,
        'client_id': CONSUMER_KEY,
        'client_secret': CONSUMER_SECRET,
        'redirect_uri': REDIRECT_URL,
        'state': 'x',
        'scope': 'psn:' + SCOPE,
        'duid': '0000000d00040080E0255A3843F84F5AAAA71D85EDB98F37'
    }

    return send_oauth(payload)


def send_oauth(payload):
    log.debug('Getting token: {}'.format(payload))

    try:
        r = requests.post(OAUTH_URL, data=payload)
    except:
        log.error('Could not connect to oauth server.')
        return False

    oauth_data = json.loads(r.text)
    oauth_data['date'] = datetime.datetime.now()

    log.debug('Got token: {}'.format(oauth_data))

    date_handler = lambda obj: obj.isoformat() if isinstance(obj, datetime.datetime) else None

    with open('.oauth', 'w') as oauth_file:
        json.dump(oauth_data, oauth_file, default=date_handler)

    return oauth_data