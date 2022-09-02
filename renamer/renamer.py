"""
    CLI tool written in Python 3 used to systemically rename files in a directory while adhering to a variety of criteria.
    Copyright (C) 2022  Kevin Tyrrell

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from argparse import ArgumentParser

import decorators as de
from directory import ConcreteDirectory


def main():
    args = ArgumentParser(description="CLI tool written in Python 3 used to systemically rename file "
                                      "in a directory while adhering to a variety of criteria")
    # Required arguments
    args.add_argument("path", type=str, help="Absolute or relative path to the directory")
    # Optional arguments
    args.add_argument("-s", "--shift", dest="shift", type=int,
                      help="Shifts all numerical values by the specified offset")
    args.add_argument("-z", "--zeroes", dest="zeroes", type=int, const=0, nargs="?",
                      help="Prepends numerical values with the specified or inferred number of leading zeroes")
    args.add_argument("-n", "--random", dest="random", type=int, const=None, nargs="?", default=False,
                      help="Shuffles numerical values using the specified seed, or randomly")
    args.add_argument("-f", "--fmt", dest="fmt", type=str, nargs="+",
                      help="Output format containing '$d' format specifier for the numerical pattern")
    args.add_argument("-e", "--ext", dest="ext", type=str,
                      help="Changes the extension of all files to the specified extension")
    args.add_argument("-c", "--consecutive", dest="consecutive", action="store_true",
                      help="Flattens numerical values such that they are all consecutive")
    args.add_argument("-m", "--mute", dest="mute", action="store_false",
                      help="Squelches the console output of filenames and their renamed filename")
    args.add_argument("-y", "--yes", dest="confirm", action="store_true",
                      help="Confirms the operation and makes changes to your file system according to the parameters")
    args = args.parse_args()

    # Process arguments
    directory = ConcreteDirectory(args.path)
    dec = de.NumeratedDecorator(directory)
    if args.shift:
        dec = de.ShifterDecorator(dec, args.shift)
    if args.fmt:
        dec = de.FormatDecorator(dec, args.fmt)
    if args.consecutive:
        dec = de.FlattenDecorator(dec)
    if args.random is not False:
        dec = de.RandomizeDecorator(dec, args.random)
    if args.zeroes is not None:
        dec = de.ZeroesDecorator(dec, args.zeroes)
    if args.ext:
        dec = de.ExtensionDecorator(dec, args.ext)
    dec.operate()  # Perform operations according to decorators

    if args.mute:
        for old, new in sorted(directory.get_files().items(), key=lambda x: x[1].num):
            print("Renaming [{}]\n\t--> [{}]".format(old, str(new)))
    if args.confirm:
        directory.save_files()


if __name__ == '__main__':
    main()
