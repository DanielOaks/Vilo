#!/usr/bin/env python3
"""
vilo.py
Copyright 2011 Daniel Oakley <danneh@danneh.net>
"""

from vilob.nico import Connection

connection = Connection()

settings_path = 'settings.json'
settings = connection.parse_config_file(settings_path)
