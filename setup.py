#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Note: To use the 'upload' functionality of this file, you must:
#   $ pipenv install twine --dev

import io
import os
import sys
from shutil import rmtree
from distutils.command.clean import clean

from setuptools import find_packages, setup, Command
import core.version as version

# Package meta-data.
NAME = 'renamer_kt'
DESCRIPTION = 'CLI tool written in Python 3 used to systemically rename files in a directory while adhering to a ' \
              'variety of criteria.'
URL = 'https://github.com/KevinTyrrell/renamer'
EMAIL = 'KevinTearUl@gmail.com'
AUTHOR = 'Kevin Tyrrell'
REQUIRES_PYTHON = '>=3'
VERSION = version.VERSION

# What packages are required for this module to be executed?
REQUIRED = [
    # 'requests', 'maya', 'records',
]

# What packages are optional?
EXTRAS = {
    # 'fancy feature': ['django'],
}

# The rest you shouldn't have to touch too much :)
# ------------------------------------------------
# Except, perhaps the License and Trove Classifiers!
# If you do change the License, remember to change the Trove Classifier for that!

here = os.path.abspath(os.path.dirname(__file__))

# Import the README and use it as the long-description.
# Note: this will only work if 'README.md' is present in your MANIFEST.in file!
try:
    with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

# Load the package's __version__.py module as a dictionary.
about = {}
if not VERSION:
    project_slug = NAME.lower().replace("-", "_").replace(" ", "_")
    with open(os.path.join(here, project_slug, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__'] = VERSION


class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        #os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))
        os.system('{0} setup.py sdist'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine…')
        os.system('twine upload dist/*')

        self.status('Pushing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()


class CustomCleanCommand(clean):
    user_options = clean.user_options + [
        ('dry-run', None, 'Perform a dry run without deleting files'),
    ]

    def initialize_options(self):
        super().initialize_options()
        self.dry_run = False

    @staticmethod
    def zap_print(path: str) -> None:
        print(f"~Cleaning: {path}")

    @staticmethod
    def zap(path: str) -> None:
        CustomCleanCommand.zap_print(path)
        if os.path.isdir(path):
            rmtree(path)
        else:
            os.remove(path)

    def run(self):
        # Call the parent's run() method
        super().run()

        clean_search = [  # Files to search for using walk / substring matches
            ('src', '__pycache'),
            ('.', 'egg-info')
        ]
        clean_target = [  # Delete specific directories
            'dist',
            'build',
            'out',
        ]

        # Only delete files if a non-dry run was desired
        zapper = CustomCleanCommand.zap_print if self.dry_run else CustomCleanCommand.zap

        for path, sub_str in clean_search:
            for root, dirs, files in os.walk(path):
                for name in files + dirs:
                    if sub_str in name:
                        zapper(os.path.join(root, name))
        for directory in clean_target:
            if os.path.exists(directory):
                zapper(directory)


PACKAGES = find_packages(where='src', exclude=["tests", "*.tests", "*.tests.*", "tests.*"])
if len("") > 0:  # Only set '>=' for debugging purposes.
    print("Discovered packages:")  # Print the list of discovered packages
    for package in PACKAGES:
        print("PACKAGE FOUND:", package)


# Where the magic happens:
setup(
    name=NAME,
    version=about['__version__'],
    description=DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=PACKAGES,
    package_dir={"":"src"},
    # If your package is a single module, use this instead of 'packages':
    # py_modules=['mypackage'],
    entry_points={
        'console_scripts': [
            'renamer = core.renamer:main',
        ],
    },
    install_requires=REQUIRED,
    extras_require=EXTRAS,
    include_package_data=True,
    zip_safe=True,
    license='GPL-3.0',
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
    keywords="file renaming, CLI tool, Python 3, naming schemes, file organization, file sorting, file management, "
             "batch renaming, file renaming tool",
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
        'clean': CustomCleanCommand,
    },
)
