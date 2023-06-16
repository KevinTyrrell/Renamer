# Renamer
> CLI tool written in Python 3 used to systemically rename files in a directory while adhering to a variety of criteria.

<!---
[![NPM Version][npm-image]][npm-url]
[![Build Status][travis-image]][travis-url]
[![Downloads Stats][npm-downloads]][npm-url]
--->

This program attempts to emulate the simplicity of the [CLI program FFmpeg](https://github.com/FFmpeg/FFmpeg) but for renaming files. Basic operations are straight-forward, while complex operations only invovle adding more flags and parameters to your operation. A directory with files that contain some numerical pattern are all that's required to get started. The application is well-paired for other software that require strict naming schemes, such as Plex, Kodi, or image managers.

![](res/HeaderImage.png)

## Installation

[![PyPI](https://img.shields.io/pypi/v/renamer_kt.svg)](https://pypi.org/project/renamer_kt/)


Install `renamer-kt` using `pip`:

### bash

```sh
pip install renamer-kt
```

*Make sure you have Python and `pip` installed.*

## Usage

| **Operation** | **Flag** | **Flag(Formal)** | **Parameter(s)**     | **Example**     | **Description**                                                                          |
|---------------|----------|------------------|----------------------|-----------------|------------------------------------------------------------------------------------------|
| _Shift_       | -s       | --shift          | Number Shift (int)   | --shift -1      | Shifts all numerical values by the specified offset                                      |
| _Zeroes_      | -z       | --zeroes         | Leading Zeroes [int] | -z 3            | Prepends numerical values with the specified or inferred number of leading zeroes        |
| _Format_      | -f       | --fmt            | Output Format (str)  | -f "Episode $d" | Customizes filename output ([see wiki](https://github.com/KevinTyrrell/Renamer/wiki/Format-Operator) for usage)|
| _Extension_   | -e       | --ext            | File Extension (str) | --ext png       | Changes the extension of all files to the specified extension                            |
| _Random_      | -n       | --random         | Random Seed [int]    | -n 839693       | Shuffles numerical values using the specified seed, or randomly                          |
| _Consecutive_ | -c       | --consecutive    |                      |                 | Flattens numerical values such that they are all consecutive                             |
| _Mute_        | -m       | --mute           |                      |                 | Squelches the console output of filenames and their renamed filename                     |
| _Confirm_     | -y       | --yes            |                      |                 | Confirms the operation and makes changes to your file system according to the parameters |

## Usage Examples

**The following usage snippets use this directory as a template:**
```
mydir/
  2021vacation0001.jpeg
  2021vacation0003.jpeg
  2021vacation0004.jpeg
  2021vacation0010.jpeg
```

#### Clean-up
> e.g. 1.jpeg, 3.jpeg, 4.jpeg, 10.jpeg
```sh
renamer mydir
```

#### Formalize & Fix Ordering
> 01.jpeg, 02.jpeg, 03.jpeg, 04.jpeg
```sh
renamer mydir -z 1 -c
```

#### Format & Modify Extension
> 2021 Vacation - 1.png, 2021 Vacation - 3.png, 2021 Vacation - 4.png, 2021 Vacation - 10.png
```sh
renamer mydir -e png -f "2021 Vacation - $d"
```

#### Shift & Flatten
> 4.jpeg, 5.jpeg, 6.jpeg, 7.jpeg
```sh
renamer mydir -s 3 -c
```


## Meta

Kevin Tyrrell – [KevinTearUl@gmail.com](mailto:KevinTearUl@gmail.com)

Distributed under the GPL3 license. See ``LICENSE`` for more information.

[https://github.com/KevinTyrrell](https://github.com/KevinTyrrell/)

## Contributing

1. Fork it (<https://github.com/KevinTyrrell/Renamer>)
2. Create your feature branch (`git checkout -b feature/fooBar`)
3. Commit your changes (`git commit -am 'Add some fooBar'`)
4. Push to the branch (`git push origin feature/fooBar`)
5. Create a new Pull Request

<!-- Markdown link & img dfn's
[npm-image]: https://img.shields.io/npm/v/datadog-metrics.svg?style=flat-square
[npm-url]: https://npmjs.org/package/datadog-metrics
[npm-downloads]: https://img.shields.io/npm/dm/datadog-metrics.svg?style=flat-square
[travis-image]: https://img.shields.io/travis/dbader/node-datadog-metrics/master.svg?style=flat-square
[travis-url]: https://travis-ci.org/dbader/node-datadog-metrics
[wiki]: https://github.com/yourname/yourproject/wiki
-->
