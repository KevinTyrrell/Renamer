#!/usr/bin/env python
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
from ntpath import basename
from os import listdir, rename
from os.path import isdir, isfile, join, splitext
from re import findall

parser = ArgumentParser(description = "Renames all files in a directory (non-recursive) such that they are numerical (starting at one) and continuous.")
parser.add_argument('path', type = str, help = "Full path to the TV Show directory.")
parser.add_argument('-c', dest = "confirm", action = 'store_true', default = False, help = "Confirms the command to make changes to the file system")
parser.add_argument('-l', dest = "leading", action = 'store_true', default = False, help = "Disables leading zeroes for output file names")
parser.add_argument('-x', dest = "displacement", default = 0, type = int, help = "Amount to add or subtract to each episode number.")

# Check the user's arguments to ensure their validity.
args = parser.parse_args()
dir_path = args.path.strip()
if (not isdir(dir_path)):
    raise Exception("The following path is not a valid directory: " + dir_path)
dir_name = basename(dir_path)

# Retrieves all files or directories in a specified directory.
def filter_files(path_to_dir: str, dirs_or_files: bool) -> list:
    return [f for f in listdir(path_to_dir) if isdir(join(path_to_dir, f))] if dirs_or_files else [f for f in listdir(path_to_dir) if isfile(join(path_to_dir, f))]

# Attempts to parse a file path or file name into an integer.
def parse_file_name(path_or_fname: str) -> int:
    path_or_fname = splitext(path_or_fname)[0]
    path_or_fname = findall(r"\d+", path_or_fname)
    l = len(path_or_fname)
    if l == 0:
        return None
    return int(path_or_fname[l - 1])

# Counts the number of digits in an integer.
def num_digits(n: int):
    n = abs(n)
    i = 1
    while n > 9:
        n //= 10
        i += 1
    return i

# Places leading zeroes behind an integer if needed.
def lead_zeroes(num: int, max_digits: int) -> str:
    if args.leading is True:
        return str(num)
    return "0" * max(max_digits - num_digits(num), 0) + str(num)
    
files = filter_files(dir_path, False)
file_num_map = { }
for f in files:
    n = parse_file_name(f)
    if n != None:
        file_num_map[f] = n
max_digits = num_digits(len(file_num_map) + args.displacement)
files = [x for x in sorted(file_num_map, key=lambda k: file_num_map[k])]

# Loop from back if displacement is positive, preventing the overwriting of existing files.
for i in (range(len(files)) if args.displacement <= 0 else range(len(files) - 1, -1, -1)):
    new_name = lead_zeroes(i + 1 + args.displacement, max_digits) + splitext(files[i])[1]
    
    print("Old: " + files[i])
    print("New: " + new_name)
    
    new_path = join(dir_path, new_name)
    if args.confirm:
        if isfile(new_path):
            print("WARNING: Skipping since path already exists: " + new_path)
            continue
            #print("Please press any key to continue.")
            #input()
        rename(join(dir_path, files[i]), new_path)
print("Done")
