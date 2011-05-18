#!/usr/bin/env python3
"""
helper.py
Copyright 2011 Daniel Oakley <danneh@danneh.net>
"""

def splitnum(line, split_num=1, split_char=' '):
    temp_list_in = line.split(split_char)
    
    if split_num > 0:
        list_out = []
        
        for i in range(split_num):
            list_out.append(temp_list_in[0])
            del temp_list_in[0]
        
        string_out = ''
        for string in temp_list_in:
            string_out += string + split_char
        
        string_out = string_out[:-1] # remove last char
        
        list_out.append(string_out)
        
        return (list_out)
    
    else:
        return None

def askok(prompt, blank=''):
    while True:
        ok = input(prompt).lower().strip()
        
        try:
            if ok[0] == 'y':
                return True
            elif ok[0] == 'n':
                return False
        
        except IndexError:
            if blank == True:
                return True
            elif blank == False:
                return False

def printprogressbar(progress, progressboxes=10):
    print('\r  [', '#'*int((progress/100)*progressboxes) + ' '*(progressboxes-int((progress/100)*progressboxes)), ']  %d%%' % progress+(' '*(len('100')-len(str(progress)))), end='')