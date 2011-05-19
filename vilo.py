#!/usr/bin/env python3
"""
vilo.py
Copyright 2011 Daniel Oakley <danneh@danneh.net>
"""

import string
import sys
from vilob.helper import newinput
from vilob.nico import Connection

connection = Connection()
print('Vilo - NicoNico Downloader')

settings_path = 'settings.json'
settings = connection.parse_config_file(settings_path, update_settings=True)

print('')

while 1:
    media_code = newinput('media code [sm...]: ', newline=False, clearline=True).strip()
    
    contains_digits = False
    for digit in string.digits:
        if digit in media_code:
            contains_digits = True
            break
    
    if contains_digits == False:
        print('Vilo Exited')
        break
    
    connection.download_media(media_code)