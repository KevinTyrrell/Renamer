#!/usr/bin/env python3

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name='Renamer',
    version='1.0.0',
    author='Kevin Tyrrell',
    author_email='KevinTearUl@gmail.com',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KevinTyrrell/renamer",
    license="GPL-3.0",
    python_requires='>=3',
    zip_safe=True,
    description="CLI tool written in Python 3 used to systemically rename files in a directory while adhering to a "
                "variety of criteria",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
    ],
    keywords="file renaming, CLI tool, Python 3, naming schemes, file organization, file sorting, file management, "
             "batch renaming, file renaming tool",
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'renamer = src.renamer:main',
        ],
    },
)
