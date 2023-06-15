from setuptools import setup, find_packages

setup(
    name='Renamer',
    version='1.0',
    author='Your Name',
    author_email='your@email.com',
    description='A powerful command line application for renaming files',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'Renamer=renamer:main',
        ],
    },
)
