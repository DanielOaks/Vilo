#!/usr/bin/env python3
"""
vilo.py
Copyright 2011 Daniel Oakley <danneh@danneh.net>
"""

import string
from vilob.nico import Connection

connection = Connection()
print('Vilo - NicoNico Downloader')

settings_path = 'settings.json'
settings = connection.parse_config_file(settings_path, update_settings=True)

while 1:
    video = input('\nmedia code [sm...]: ').strip()
    
    contains_digits = False
    for digit in string.digits:
        if digit in video:
            contains_digits = True
            break
    
    if contains_digits == False:
        print('\nVilo Exited')
        break
    
    downloaded = connection.download_video(video)