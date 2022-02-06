#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from ntpath import basename
from os import path, listdir, rename
from os.path import isdir, isfile, join, splitext
from re import compile, finditer
from typing import List, Tuple, Dict

DIRECTORY_FORMAT = "Season {}"
EPISODE_FORMAT = "{} - s{}e{}{}"
MIN_FILE_NUM_WIDTH = 2

parser = ArgumentParser(description = "Renames TV series' filenames to the format: Show - s##e##.")
parser.add_argument('path', type = str, help = "Full path to the TV Show directory.")
#parser.add_argument('reg_exp', type = str, help = "Regular expression used on episodes.")
parser.add_argument('-c', dest = "confirm", action = 'store_true', default = False, help = "Confirms the command to make changes to the file system.")
parser.add_argument('-f', dest = "flatten", action = 'store_true', default = False, help = "Flattens episode numbers, ensuring numbering starts at '1'.")
parser.add_argument('-x', dest = "displacement", default = 0, type = int, help = "Amount to add or subtract to each episode number.")

# Check the user's arguments to ensure their validity.
args = parser.parse_args()
dir_path = args.path.strip()
if (not isdir(dir_path)):
    raise Exception("The following path is not a valid directory: " + dir_path)
dir_name = basename(dir_path)

pattern = compile("\s*(.+?)\s*\(\s*\d+\s*\)\s*")
match = pattern.match(dir_name)
if (match == None):
    raise Exception("Specified directory name does not match expected format: Show Name (Year)")
show_title = match.group(1)

# Retrieves all files or directories in a specified directory.
def filter_files(path_to_dir: str, dirs_or_files: bool) -> list:
    return [f for f in listdir(path_to_dir) if isdir(join(path_to_dir, f))] if dirs_or_files else [f for f in listdir(path_to_dir) if isfile(join(path_to_dir, f))]

"""
Searches for an interative number pattern in a directory.
Once found, the iterative number for each file is returned in a list.
The number pattern must start in the same index for each file name.
"""
def episode_nums(files: List[str]) -> List[int]:
    assert files # TODO: This should be changed to be an exception (no season folders).
    REGEXP_NUMS = "([0-9]+)" # Find all runs of numbers.
    # Indexes of the first digits of all numbers in the first filename.
    indexes = [m.start() for m in finditer(REGEXP_NUMS, splitext(files[0])[0])]
    pattern = compile(REGEXP_NUMS) # Change regex to search only start of string.
    
    def map_to_int(s: str, index: int) -> int:
        match = pattern.match(s, index)
        return None if not match else int(match.group(0))
    # Set for each number to determine which are constantly changing.
    ep_sets = [ set([ map_to_int(files[0], i) ]) for i in indexes ]
    #print(ep_sets)
    
    for i in range(1, len(files)):
        for j in range(len(indexes) - 1, -1, -1):
            h = indexes[j]
            s = ep_sets[j]
            n = map_to_int(files[i], h)
            if n in s:
                del indexes[j]
                del ep_sets[j]
            else:
                s.add(n)
    if not indexes or len(indexes) > 1:
        #print(indexes)
        raise Exception("A cohesive numerical pattern was not found the specified directories.")
    index = indexes[0]
    return [ map_to_int(f, index) for f in files ]

# Ensures episode numbers always begin at either 0 or 1.
def flatten_nums(nums: List[int]) -> None:
    assert nums
    small = min(nums)
    if small > 1:
        for i in range(len(nums)):
            nums[i] -= small - 1

season_names = filter_files(dir_path, True)
season_nums = episode_nums(season_names)
#flatten_nums(season_nums) # TODO: Find a more constructive way to implement this.
season_paths = [ join(dir_path, p) for p in season_names ]
eps_names_nums = [ ]

# Iterate through all episode directories and ensure no problems occur.
for i in range(0, len(season_names)):
    ep_names = filter_files(season_paths[i], False)
    ep_nums = episode_nums(ep_names)
    if args.flatten:
        flatten_nums(ep_nums)
    eps_names_nums.append(( ep_names, ep_nums ))

max_se = max(season_nums)
max_ep = max([ max(t[1]) for t in eps_names_nums ])
width_se = max(MIN_FILE_NUM_WIDTH, len(str(max_se)))
width_ep = max(MIN_FILE_NUM_WIDTH, len(str(max_ep)))

# Mutates the list of file numbers into strings with leading '0's.
def convert_file_nums(nums: List[int], width: int) -> None:
    assert nums
    for i in range(len(nums)):
        num_str = str(nums[i])
        nums[i] = "0" * (width - len(num_str)) + num_str
        
convert_file_nums(season_nums, width_se)
for nn in eps_names_nums:
    convert_file_nums(nn[1], width_ep)

old_partial_paths = [ ]
new_partial_paths = [ ]
for si in range(len(season_names)):
    s_name = season_names[si]               # Old Season Filename
    s_num = season_nums[si]                 # Formatted Season Number
    s_eps = eps_names_nums[si][0]           # List of old episode filenames.
    s_enums = eps_names_nums[si][1]         # List of new episode numbers.
    
    # Loop from back if displacement is positive, preventing the overwriting of existing files.
    for ei in (range(len(s_eps)) if args.displacement <= 0 else range(len(s_eps) - 1, -1, -1)):
        en = s_eps[ei]
        ext = splitext(en)[1]               # Episode file extension.
        new_name = EPISODE_FORMAT.format(show_title, s_num, int(s_enums[ei]) + args.displacement, str(ext))
        new_partial_paths.append(join(s_name, new_name))
        old_partial_paths.append(join(s_name, en))
    old_partial_paths.append(s_name)
    new_partial_paths.append(DIRECTORY_FORMAT.format(s_num))

for i in range(len(old_partial_paths)):
    print("Old: " + old_partial_paths[i])
    print("New: " + new_partial_paths[i])

if args.confirm:
    print("This operation will make changes to your file system. Press [ENTER] to continue.")
    input()
    for i in range(len(old_partial_paths)):
        rename(join(dir_path, old_partial_paths[i]), join(dir_path, new_partial_paths[i]))
print("Done.")
