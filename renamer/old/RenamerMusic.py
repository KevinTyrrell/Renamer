#!/usr/bin/env python
# -*- coding: utf-8 -*- 

import os
import re

ROOT_DIR = "D:\Plex Library\Evanescence - Fallen"
TRACK_NUM_REGEXP = "\s*(\d+)\s*.+"
TRACK_NAME_REGEXP = ".*\.\s*(.+)\s*\.[^\.]+"
DRY_RUN = True

SPACED_CHAR_REGEXP = '[\_\-]'
FILE_EXT_REGEXP = ".+\.([^\.]+)"
TRACK_DIGITS = 2
OUTPUT_FORMAT = "{} - {}.{}"

# Returns the first capture group of a regular expression, if present.
def findStr(str, regexp):
    match = re.findall(regexp, str)
    if len(match) <= 0:
        raise Exception("Could not match expression \"{}\" with String \"{}\"".format(regexp, str))
    return match[0]

def main():
    for subdir, dirs, files in os.walk(ROOT_DIR):
        for file in files:
            print("Renaming: {}".format(file))
            
            track_num = findStr(file, TRACK_NUM_REGEXP)
            track_name = findStr(file, TRACK_NAME_REGEXP)
            track_name = re.sub(SPACED_CHAR_REGEXP, ' ', track_name).strip().title()
            track_ext = findStr(file, FILE_EXT_REGEXP)
            
            #track_name = re.sub("[_\-]", " ", track_name)
            #track_name = track_name.title()

            track_num = str(int(track_num))
            track_num = (max(TRACK_DIGITS - len(track_num), 0)) * "0" + track_num
            
            output = OUTPUT_FORMAT.format(track_num, track_name, track_ext)
            print("Renamed : {}".format(output))
            if not DRY_RUN:
                os.rename(os.path.join(subdir, file), os.path.join(subdir, output))
main()
