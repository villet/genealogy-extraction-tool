### Date created
2020-07-16

### Changelog

#### 1.0.0 - 2020-07-16

##### Added
- First stable version of tool

## Data Extraction Tool for Family History Book

### Background

This is my summer 2020 project to support the effort to digitalize a family book about my father's family. Besides my personal interest on family history and data, I want to use more SQL and build extractions tools for command line - and later as an webapp.

The Tossavainen family book was finished by a single author in 1993, and it has hundreds of hand-drawn diagrams including some text pages. However, the doesn't have an index which makes is hard to find people. Also the structure and format doesn't common standards.

The Tossavainen Family Association has had a long-time desire to digitalize the book and make it available for everyone. The journey is long and needs help from several volunteers.

The first step is to make an index of all people in the book (around 5,000). The data in the index should also be combined and reviewed.

### Description

This tool was built to help extract genealogical data from a family book and save it to a PostgresSQL database. The data is meant to keep simple

### Requirements

The program requires Python version 3 and a PostgresSQL database installed.

### Files used
extract_genealogy.py

### Additional Sources

1. Malinen, P. (1993) Tossavaisia Tossavalansaaresta. Kerama, Kuopio.

2. Tossavaisten sukuseura ry (Tossavainen Family Association) https://www.tossavaiset.fi


### Acknowledges

1. PostgreSQL Python Tutorial with Practical Examples https://www.postgresqltutorial.com/postgresql-python/

2. Psycopg2 Project at PyPI https://pypi.org/project/psycopg2
