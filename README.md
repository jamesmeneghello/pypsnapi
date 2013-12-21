pypsnapi
========

A basic example of accessing PSN using Python., and a script to cull the size of your friends list.

The delete script will delete users from your friendslist to cut it down to the size specified in config.py. I wrote this
primarily because UPlay on PS4 can't handle friends lists of greater than 99 players, which breaks the fuck out of
certain games (AC4). It sorts users by their last login date, so it should cull the most inactive users first.

It's also an example of how to access the PSN API in Python. While not fully featured (obviously), it serves as an example.
You can sniff the rest of the functionality of the API by using the Android/iOS PSN app and running it through mitmproxy.

Requirements
------------

- Python 2.7
- Mechanize, Requests, Requests_oauthlib

Installation
------------

    > pip install mechanize requests requests_oauthlib

Execution
---------

    [edit config.py to add psn details and desired cull size]
    > python delete.py
    [follow prompts]
