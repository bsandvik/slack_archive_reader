from setuptools import setup, find_packages

setup(
    name='slack_archive_reader',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'emoji',
        'markdown2',
    ],
    entry_points={
        'console_scripts': [
            'slack_archive_reader = slack_archive_reader.main:main',
            'slack-archive-reader = slack_archive_reader.main:main',
        ],
    },
    description='A tool for reading and searching Slack JSON export files.',
    author='Bjornar Sandvik',
    author_email='bsandvik@gmail.com',
    url='https://github.com/bsandvik/slack_archive_reader',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
