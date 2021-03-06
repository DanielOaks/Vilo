#!/usr/bin/env python3
"""
nico.py
Copyright 2011 Daniel Oakley <danneh@danneh.net>
"""

import json
import http.cookiejar
import urllib.request, urllib.parse
#import chardet
import os
from time import time
from .helper import askok, printprogressmeter, bytestostr
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
    
    def login(self, email, password, site=None):
        login_url = 'https://secure.nicovideo.jp/secure/login'
        if site:
            login_url += '?site=' + site
        login_values = {
            'mail' : email,
            'password' : password,
        }
        login_params = urllib.parse.urlencode(login_values)
        login_params = login_params.encode('utf-8')
        login_request = urllib.request.Request(login_url, login_params)
        login_open = urllib.request.urlopen(login_request)
        login_open.close()
    
    def download_media(self, media):
        try:
            os.makedirs('media')
        except OSError:
            if os.path.isdir('media'):
                pass
            else:
                raise
        
        outcome = False
        if 'sm' in media:
            outcome = self.download_douga(media)
            print('')
            try:
                self.cj.clear('.nicovideo.jp', '/', 'nicohistory')
            except:
                pass
        elif 'im' in media:
            outcome = self.download_seiga(media)
            print('')
            try:
                self.cj.clear('seiga.nicovideo.jp')
            except:
                pass
        return outcome
    
    def download_douga(self, video):
        if len(self.cj) is 0:
            self.login(self.email, self.password, site='niconico')
        
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
                print('video [%s] downloading as %s' % (video, video_type))
                if True:
                    full_open = urllib.request.urlopen(download_results['url'])
                    local_file = open('media/'+video+'.'+video_type, 'wb')
                    
                    try:
                        block_size = 1024*8
                        block_num = 0
                        read = 0
                        size = int(full_open.info()['Content-Length'])
                        previous_percent = 0
                        while 1:
                            block = full_open.read(block_size)
                            if not block:
                                break
                            read += len(block)
                            local_file.write(block)
                            block_num += 1
                            
                            current_percent = int((read / size) * 100)
                            #printprogressmeter(current_percent, l_indent=2, r_indent=6)
                            #percent = ' '
                            #percent += ' ' * int(4 - len(str(current_percent) + '%'))
                            #percent += str(current_percent) + '%'
                            #print(percent, end='')
                            if current_percent != previous_percent:
                                previous_percent = current_percent
                                print(str(current_percent) + '%% Complete')
                    finally:
                        print('')
                        local_file.close()
                        full_open.close()
                else:
                    filename, headers = urllib.request.urlretrieve(download_results['url'], video+'__.'+video_type)
                print('video [%s] downloaded' % video)
                return True
            except urllib.error.HTTPError as e:
                print('video [%s] could not be downloaded : %d' % (video, e.code))
                return False
            except urllib.error.URLError as e:
                print('video [%s] could not be downloaded : %d' % (video, e.code))
                return False
        else:
            print('video [%s] could not be downloaded : invalid video' % video)
            return False
    
    def download_seiga(self, image):
        if len(self.cj) is 0:
            self.login(self.email, self.password, site='seiga')
        
        download_url = 'http://seiga.nicovideo.jp/image/source?id=' + image[2:]
        
        try:
            download_open = urllib.request.urlopen(download_url)
        except urllib.error.HTTPError as e:
            print('image [%s] could not be downloaded : %d' % (image, e.code))
            return False
        except urllib.error.URLError as e:
            print('image [%s] could not be downloaded : %d' % (image, e.code))
            return False
        
        local_file = open('media/'+image+'.jpg', 'wb')
        
        print('image [%s] downloading' % image)
        try:
            block_size = 1024*8
            block_num = 0
            read = 0
            size = int(download_open.info()['Content-Length'])
            while 1:
                block = download_open.read(block_size)
                if not block:
                    break
                read += len(block)
                local_file.write(block)
                block_num += 1
                
                current_percent = int((read / size) * 100)
                printprogressmeter(current_percent, l_indent=2, r_indent=6)
                percent = ' '
                percent += ' ' * int(4 - len(str(current_percent) + '%'))
                percent += str(current_percent) + '%'
                print(percent, end='')
        finally:
            print('')
            local_file.close()
            download_open.close()
        print('image [%s] downloaded' % image)
        return True
    
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
            new_email = input(' email ['+email+']: ').strip()
            if new_email != '':
                email = new_email
        except:
            new_email = ''
            while new_email == '':
                new_email = input(' email: ').strip()
            email = new_email
        
        #>> password
        password = ''
        try:
            password = settings['password']
            new_password = getpass(' password ['+('*'*len(password))+']: ').strip()
            if new_password != '':
                password = new_password
        except:
            new_password = ''
            while new_password == '':
                new_password = getpass(' password: ').strip()
            password = new_password
        
        #>> finished
        return {
            'email' : email,
            'password' : password,
        }
    
    def load_settings(self, settings):
        try:
            self.email = settings['email']
            self.password = settings['password']
            
            self.login(self.email, self.password)
        except:
            print('error (load_settings): cannot parse settings dictionary')