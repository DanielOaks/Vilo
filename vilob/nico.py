#!/usr/bin/env python3
"""
nico.py
Copyright 2011 Daniel Oakley <danneh@danneh.net>
"""

import json
import http.cookiejar
import urllib.request, urllib.parse
import chardet
from time import time
from .helper import askok, printprogressbar
from getpass import getpass

class Connection:
    """ Provides a connection to the target site, contains methods for
        interacting with it. """
    
    def __init__(self):
        self.email = ''
        self.password = ''
        
        self.cj = http.cookiejar.CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cj))
        urllib.request.install_opener(self.opener)
    
    def login(self, email, password, video=None):
        login_url = 'https://secure.nicovideo.jp/secure/login?site=niconico'
        login_values = {
            'mail' : email,
            'password' : password,
        }
        if video:
            login_values['next_url'] = '/watch/' + str(video)
        login_params = urllib.parse.urlencode(login_values)
        login_params = login_params.encode('utf-8')
        login_request = urllib.request.Request(login_url, login_params)
        login_open = urllib.request.urlopen(login_request)
        login_open.close()
    
    def download_video(self, video):
        if len(self.cj) is 0:
            self.login(self.email, self.password, video)
        
        download_values = {
            #'ts' : str(time()).split('.')[0],
            'as3' : '1',
            #'lo' : '0',
        }
        download_params = urllib.parse.urlencode(download_values)
        download_params = '?' + str(download_params)
        download_url = 'http://www.nicovideo.jp/api/getflv/' + video + download_params
        download_open = urllib.request.urlopen(download_url)
        
        download_results = {}
        download_success = False
        for pair in download_open.read().decode('utf-8').split('&'):
            title, value = pair.split('=')
            download_results[title] = urllib.parse.unquote(value)
            if title == 'url':
                download_success = True
        #for title in download_results:
        #    print(' ', title, '=', download_results[title])
        download_open.close()
        
        if download_success:
            # set download cookie
            urllib.request.urlopen('http://www.nicovideo.jp/watch/'+video)
            
            video_type = ''
            try:
                if False:
                    thread_url = 'http://www.nicovideo.jp/api/getthreadkey?thread=' + download_results['thread_id']
                    thread_url += '&ts=' + str(time()).split('.')[0]
                    print(thread_url)
                    thread_open = urllib.request.urlopen(thread_url)
                    print(thread_open.read().decode('utf-8'))
                
                if '?s=' in download_results['url']:
                    video_type = 'swf'
                elif '?m=' in download_results['url']:
                    video_type = 'mp4'
                else:
                    video_type = 'flv'
                print('downloading video [%s]' % video)
                if True:
                    full_open = urllib.request.urlopen(download_results['url'])
                    local_file = open(video+'.'+video_type, 'wb')
                    
                    try:
                        block_size = 1024*8
                        block_num = 0
                        read = 0
                        size = int(full_open.info()['Content-Length'])
                        while 1:
                            block = full_open.read(block_size)
                            if not block:
                                break
                            read += len(block)
                            local_file.write(block)
                            block_num += 1
                            printprogressbar((read/size)*100)
                    finally:
                        print('')
                        local_file.close()
                        full_open.close()
                else:
                    filename, headers = urllib.request.urlretrieve(download_results['url'], video+'__.'+video_type)
                print('video [%s] downloaded' % video)
            except urllib.error.HTTPError as e:
                print('HTTP Error', e.code, ':', download_results['url'])
                return
            except urllib.error.URLError as e:
                print('URL Error:', e.code, ':', download_results['url'])
                return
        else:
            print('video [%s] cound not be downloaded' % video)
    
    
    def parse_config_file(self, settings_path, update_settings=False):
        #>> deal with config file
        settings = None
        try:
            settings_file = open(settings_path, 'r')
            settings = json.loads(settings_file.read())
            settings_file.close()
        except:
            settings = None
        
        if update_settings:
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
            if askok('email ['+email+']: ', blank=True):
                pass
            else:
                raise Exception
        except:
            email = input('new email address: ')
        
        #>> password
        password = ''
        try:
            password = settings['password']
            if askok('password ['+('*'*len(password))+']: ', blank=True):
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
        try:
            self.email = settings['email']
            self.password = settings['password']
        except:
            print('error (load_settings): cannot parse settings dictionary')