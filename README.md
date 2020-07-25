### Date created
2020-07-16

### Changelog

#### 1.0.0 - 2020-07-16

##### Added
- First stable version of tool

#### 1.0.1 - 2020-07-19

##### Added
- Extended person extraction for entire family line

## Data Extraction Tool for Family History Book

### Background

This is my on-going summer 2020 project to support the effort to digitalize a family book about my father's family. Besides my personal interest in family history and data, I want to use more SQL and build extractions tools on the command line—and later as a web app.

The Tossavainen family book was finished by a single author in 1993, and it has hundreds of hand-drawn diagrams including some text pages. However, the book doesn't have an index which makes it hard to search for people. Also, the structure and format don't follow common standards.

The Tossavainen Family Association has had a long-time desire to digitalize the book and make it available for everyone. The journey is long and needs help from several volunteers.

The first step is to make an index of all people in the book (around 5,000 excluding duplicate persons). The data in the index should also be combined and reviewed.

### Description

This tool was built to speed-up the extraction of genealogical data from a family book and save it to a PostgresSQL database. The input data is meant to keep simple but covers most personal data (names, birth and death) and relationships (marriage and children).

### Requirements

The program requires Python version 3 and a PostgresSQL database installed.

### Files used
extract_genealogy.py – Data extraction tool

xxx.py — Data review tool

### Additional Sources

1. Malinen, P. (1993) Tossavaisia Tossavalansaaresta. Kerama, Kuopio.

2. Tossavaisten sukuseura ry (Tossavainen Family Association) https://www.tossavaiset.fi


### Acknowledges

1. PostgreSQL Python Tutorial with Practical Examples https://www.postgresqltutorial.com/postgresql-python/

2. Psycopg2 Project at PyPI https://pypi.org/project/psycopg2
