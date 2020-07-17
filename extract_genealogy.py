import sys
import psycopg2
from config import config

INPUT_FILE = 'input.html'

def initialize_entry(page_number):
    """
    Inserts an entry into database

    Args:
        (integer) page - Page number
    Returns:
        (int) entry_id - Entry ID
    """

    sql = """INSERT INTO entries(page_number) VALUES({})
          RETURNING entry_id;"""

    conn = None
    entry_id = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql.format(page_number))
        # get the generated UID back
        entry_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return entry_id

def update_names(entry_id, first_names, last_name):
    """
    Update person's first and last names

    Args:
        (integer) entry_id - Entry ID
        (string) first_names - Person's first and middle names
        (string) last_name - Person's last (maiden name)
    Returns:
        (int) updated_rows - How many rows updated
    """

    sql = """ UPDATE entries
                SET first_names = '{}', last_name = '{}'
                WHERE entry_id = {}"""

#    # Change ' with '' for SQL input compatibility
#    if name.find('\'') != -1:
#        name.replace('\'', '\'\'')


    conn = None
    updated_rows = 0
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute(sql.format(first_names, last_name, entry_id))
        # get the number of updated rows
        updated_rows = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return updated_rows

def update_date(entry_id, event_type, date):
    """
    Update a date value in an entry

    Args:
        (integer) entry_id - Entry ID
        (string) event_type - Type of event matching with a column (birth etc.)
        (string) date - Date in "YYYY-MM-DD" format
    Returns:
        (int) updated_rows - How many rows updated
    """

    sql = """ UPDATE entries
                SET {}_date = {}
                WHERE entry_id = {}"""

    if len(date) == 0:
        date = 'NULL'
    else:
        date = "'" + date + "'" # added string need to be within '-characters

    conn = None
    updated_rows = 0
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute(sql.format(event_type, date, entry_id))
        # get the number of updated rows
        updated_rows = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return updated_rows

def update_place(entry_id, event_type, place):
    """
    Update a place value in an entry

    Args:
        (integer) entry_id - Entry ID
        (string) event_type - Type of event matching with a column (birth etc.)
        (string) place - Name of place
    Returns:
        (int) updated_rows - How many rows updated
    """

    sql = """ UPDATE entries
                SET {}_place = {}
                WHERE entry_id = {}"""

#    # Change ' with '' for SQL input compatibility
#    if name.find('\'') != -1:
#        name.replace('\'', '\'\'')

    if len(place) == 0:
        place = 'NULL'
    else:
        place = "'" + place + "'" # added string need to be within '-characters

    conn = None
    updated_rows = 0
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute(sql.format(event_type, place, entry_id))
        # get the number of updated rows
        updated_rows = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return updated_rows

def convert_date_dmy_to_ymd(date):
    """
    Conver DD.MM.YYYY (German) date format to YYYY-MM-DD (ISO) date format

    Args:
        (string) date - date in DD.MM.YYYY format
    Returns:
        (string) date - date in YYYY-MM-DD format (or original if not able to convert)
    """

    if date:
        date_parts = date.split('.')
        if len(date_parts) == 3:
            # CHECK LENGTH (2/4 chars), NUMBER AND CONTENT (X is ok)
            date = date_parts[2] + '-' + date_parts[1] + '-' + date_parts[0]
        elif len(date_parts) == 2:
            date = date_parts[1] + date_parts[0] + '-XX'
        elif len(date_parts) == 1:
            date = date_parts[0] + '-XX-XX'
        else:
            print('Not a valid date: {}. Date not converted.'.format(date))
    return date

def update_number_of_children(entry_id, number_of_children):
    """
    Update number of children in an entry

    Args:
        (integer) entry_id - Entry ID
        (integer) number_of_children - Number of known children
    Returns:
        (int) updated_rows - How many rows updated
    """

    sql = """ UPDATE entries
                SET number_of_children = {}
                WHERE entry_id = {}"""

    if len(number_of_children) == 0:
        number_of_children = 'NULL'

    conn = None
    updated_rows = 0
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute(sql.format(number_of_children, entry_id))
        # get the number of updated rows
        updated_rows = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return updated_rows

def update_comments(entry_id, comments):
    """
    Update a comment value in an entry

    Args:
        (integer) entry_id - Entry ID
        (string) comments - Comments about the entry
    Returns:
        (int) updated_rows - How many rows updated
    """

    sql = """ UPDATE entries
                SET comments = {}
                WHERE entry_id = {}"""

    if len(comments) == 0:
        comments = 'NULL'
    else:
        comments = "'" + comments + "'" # added string need to be within '-characters

#    # Change ' with '' for SQL input compatibility
#    if name.find('\'') != -1:
#        name.replace('\'', '\'\'')

    conn = None
    updated_rows = 0
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the UPDATE  statement
        cur.execute(sql.format(comments, entry_id))
        # get the number of updated rows
        updated_rows = cur.rowcount
        # Commit the changes to the database
        conn.commit()
        # Close communication with the PostgreSQL database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return updated_rows


def get_entry(entry_id):
    """
    Get and display an entry from database

    Args:
        (integer) entry_id - Entry ID
    """

    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT * FROM entries WHERE entry_id = {}".format(entry_id))
        print("The number of parts: ", cur.rowcount)
        row = cur.fetchone()

        while row is not None:
            print(row)
            row = cur.fetchone()

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def main():
    """ Main function """

    page_number = input('Provide page of extraction: ')
    # CHECK IF PAGE IS REALLY INT

    add_more_entries = True
    while add_more_entries:

        print('Add a new entry in database:')

        # MAKE ENTRY AS AN OBJECT
        first_names = input('- First names: ')
        last_name = input('- Last name: ')

        birth_date = input('- Birth date: ') # different date formats
        birth_place = input('- Birth place: ')
        death_date = input('- Death date: ')
        death_place = input('- Death place: ')
        marriage_date = input('- Married date: ')
        marriage_place = input('- Married place: ')
        number_of_children = input('- Number of children: ')
        comments = input('- Additional comments: ')

        # Checks and adds user to database
        entry_id = initialize_entry(page_number)
        update_names(entry_id, first_names, last_name)

        update_date(entry_id, 'birth', convert_date_dmy_to_ymd(birth_date))
        update_place(entry_id, 'birth', birth_place)

        update_date(entry_id, 'death', convert_date_dmy_to_ymd(death_date))
        update_place(entry_id, 'death', death_place)

        update_date(entry_id, 'marriage', convert_date_dmy_to_ymd(marriage_date))
        update_place(entry_id, 'marriage', marriage_place)

        update_number_of_children(entry_id, number_of_children)
        update_comments(entry_id, comments)

        get_entry(entry_id)


if __name__ == "__main__":
    main()
