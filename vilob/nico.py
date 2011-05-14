#!/usr/bin/env python3
"""
nico.py
Copyright 2011 Daniel Oakley <danneh@danneh.net>
"""

import json
from helper import askok
from getpass import getpass

class Connection:
    """ Provides a connection to the target site, contains methods for
        interacting with it. """
    
    def __init__(self):
        pass
    
    
    def login(self, email, password):
        pass
    
    def download_video(self, video):
        pass
    
    
    def parse_config_file(self, settings_path):
        #>> deal with config file
        settings = None
        try:
            settings_file = open(settings_path, 'r')
            settings = json.loads(settings_file.read())
            settings_file.close()
        except:
            settings = None
        
        settings = self.prompt_settings(settings)
        
        try:
            settings_file = open(settings_path, 'w')
            settings_file.write(json.dumps(settings, sort_keys=True, indent=4))
            settings_file.close()
        except:
            print('Failed to save configuration file:', settings_path)
        
        #>> load settings
        self.load_settings(settings)
    
    def prompt_settings(self, settings=None):
        #>> email address
        email = ''
        try:
            email = settings['email']
            if askok('email ['+email+'] y/n: ', blank=True):
                pass
            else:
                raise Exception
        except:
            email = input('new email address: ')
        
        #>> password
        password = ''
        try:
            password = settings['password']
            if askok('password ['+('*'*len(password))+'] y/n: ', blank=True):
                pass
            else:
                raise Exception
        except:
            password = getpass('new password: ')
        
        #>> finished
        return {
            'email' : email,
            'password' : password,
        }
    
    def load_settings(self, settings):
        pass