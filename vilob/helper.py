#!/usr/bin/env python3
"""
helper.py
Copyright 2011 Daniel Oakley <danneh@danneh.net>
"""

import os
import sys

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
    print('\r [', '#'*int((progress/100)*progressboxes) + ' '*(progressboxes-int((progress/100)*progressboxes)), ']  %d%%' % progress+(' '*(len('100')-len(str(progress)))), end='')

def printprogressmeter(percent, boxes=None, l_indent=1, r_indent=1, newline=False):
    output = '\r'
    output += ' ' * l_indent
    output += '[ '
    
    if boxes == None:
        terminalinfo = terminfo()
        boxes = terminalinfo['x']
        boxes = boxes - len(output) - 2 - r_indent
    output += progressmeter(percent, boxes)
    output += ' ]'
    if newline:
        print(output)
    else:
        print(output, end='')

def progressmeter(percent, boxes=10):
    filledboxes = (percent / 100) * boxes
    (filledboxes, splitbox) = str(filledboxes).split('.')
    splitbox = float('0.'+splitbox)
    
    progressmeter = '#' * int(filledboxes)
    if splitbox == 0:
        progressmeter += ' ' * (boxes - int(filledboxes))
    elif splitbox < 0.5:
        progressmeter += '-'
        progressmeter += ' ' * (boxes - int(filledboxes) - 1)
    else:
        progressmeter += '='
        progressmeter += ' ' * (boxes - int(filledboxes) - 1)
    
    return progressmeter

def bytestostr(bytes):
    if bytes >= 1099511627776:
        terabytes = int(bytes / 1099511627776)
        output = str(terabytes) + 'T'
    #   - = #
    elif bytes >= 1073741824:
        gigabytes = int(bytes / 1073741824)
        output = str(gigabytes) + 'G'
    
    elif bytes >= 1048576:
        megabytes = int(bytes / 1048576)
        output = str(megabytes) + 'M'
    
    elif bytes >= 1024:
        kilobytes = int(bytes / 1024)
        output = str(kilobytes) + 'K'
    
    else:
        output = str(int(bytes)) + 'b'
    
    return output


def _fallback_newinput(prompt, stream=None, newline=None, clearline=False):
    output = input(prompt)

def _win_newinput(prompt, stream=None, newline=True, clearline=False):
    if sys.stdin is not sys.__stdin__:
        return _fallback_newinput(prompt, stream)
    import msvcrt
    for c in prompt:
        msvcrt.putwch(c)
    
    pw = ""
    pwcursor = 0
    arrowkey = False
    
    while 1:
        c = msvcrt.getwch()
        if c == '\r' or c == '\n':
            if newline:
                msvcrt.putwch('\n')
            break
        if c == '\003':
            raise KeyboardInterrupt
        if c == '\b':
            if len(pw) > 0 and pwcursor > 0:
                msvcrt.putwch('\b')
                msvcrt.putwch(' ')
                msvcrt.putwch('\b')
                pwcursor -= 1
                pw = pw[:pwcursor] + pw[pwcursor+1:]
                pw += ' '
                for ch in pw[pwcursor:]:
                    msvcrt.putwch(' ')
                for ch in pw[pwcursor:]:
                    msvcrt.putwch('\b')
                for ch in pw[pwcursor:]:
                    msvcrt.putwch(ch)
                for ch in pw[pwcursor:]:
                    msvcrt.putwch('\b')
                pw = pw[:-1]
        elif c.encode('utf-8') == b'\xc3\xa0':
            arrowkey = True
            continue
        elif arrowkey:
            if c == 'K': #leftarrow
                if pwcursor > 0:
                    pwcursor -= 1
                    msvcrt.putwch('\b')
                arrowkey = False
                continue
            elif c == 'M': #rightarrow
                if pwcursor < len(pw):
                    pwcursor += 1
                    msvcrt.putwch(pw[pwcursor-1])
                arrowkey = False
                continue
            elif c == 'G': #home
                while pwcursor > 0:
                    pwcursor -= 1
                    msvcrt.putwch('\b')
                arrowkey = False
                continue
            elif c == 'O': #end
                while pwcursor < len(pw):
                    pwcursor += 1
                    msvcrt.putwch(pw[pwcursor-1])
                arrowkey = False
                continue
            else:
                arrowkey = False
                continue
        else:
            pw = pw[:pwcursor] + c + pw[pwcursor:]
            for ch in pw[pwcursor:]:
                msvcrt.putwch(ch)
            for ch in pw[pwcursor+1:]:
                msvcrt.putwch('\b')
            pwcursor += 1
    
    if clearline:
        while pwcursor < len(pw):
            msvcrt.putwch(' ')
            pwcursor += 1
        for c in pw:
            msvcrt.putwch('\b')
            msvcrt.putwch(' ')
            msvcrt.putwch('\b')
        for c in prompt:
            msvcrt.putwch('\b')
            msvcrt.putwch(' ')
            msvcrt.putwch('\b')
    return pw

# bind newinput to correct os-specific function
try:
    import termios
    # it's possible there is an incompatible termios from the
    # McMillan Installer, make sure we have a UNIX-compatible termios
    termios.tcgetattr, termios.tcsetattr
except (ImportError, AttributeError):
    try:
        import msvcrt
    except ImportError:
        newinput = _fallback_newinput
    else:
        newinput = _win_newinput
else:
    #newinput = _unix_newinput
    newinput = _fallback_newinput


def _fallback_terminfo():
    x = None
    y = None
    
    return {
        'x' : x,
        'y' : y,
    }
    
def _win_terminfo():
    from ctypes import windll, create_string_buffer
    h = windll.kernel32.GetStdHandle(-12)
    csbi = create_string_buffer(22)
    res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
    
    if res:
        import struct
        
        (bufx, bufy, curx, cury, wattr, left, top, right, bottom, maxx, maxy)\
        = struct.unpack("hhhhHhhhhhh", csbi.raw)
        
        x = right - left + 1
        y = bottom - top + 1
        
    else:
        x = None
        y = None
    
    return {
        'x' : x,
        'y' : y,
    }

def _unix_terminfo():
    x = int(os.popen('tput cols', 'r').readline())
    y = int(os.popen('tput lines', 'r').readline())
    
    return {
        'x' : x,
        'y' : y,
    }

# bind terminfo to correct os-specific function
try:
    import termios
    # it's possible there is an incompatible termios from the
    # McMillan Installer, make sure we have a UNIX-compatible termios
    termios.tcgetattr, termios.tcsetattr
except (ImportError, AttributeError):
    try:
        import msvcrt
    except ImportError:
        terminfo = _fallback_terminfo
    else:
        terminfo = _win_terminfo
else:
    #newinput = _unix_newinput
    terminfo = _fallback_terminfo