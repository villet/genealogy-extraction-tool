import psycopg2
from config import config

def initialize_person(page_number):
    """
    Inserts a person into database

    Args:
        (integer) page - Page number
    Returns:
        (int) person_id - Person ID
    """

    sql = """INSERT INTO persons(page_number) VALUES({})
          RETURNING person_id;"""

    conn = None
    person_id = None
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
        person_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return person_id

def update_names(person_id, first_names, last_name):
    """
    Update person's first and last names

    Args:
        (integer) person_id - Person ID
        (string) first_names - Person's first and middle names
        (string) last_name - Person's last (maiden name)
    Returns:
        (int) updated_rows - How many rows updated
    """

    sql = """ UPDATE persons
                SET first_names = '{}', last_name = '{}'
                WHERE person_id = {}"""

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
        cur.execute(sql.format(first_names, last_name, person_id))
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

def update_date(person_id, event_type, date):
    """
    Update a date value in a person

    Args:
        (integer) person_id - Person ID
        (string) event_type - Type of event matching with a column (birth etc.)
        (string) date - Date in "YYYY-MM-DD" format
    Returns:
        (int) updated_rows - How many rows updated
    """

    sql = """ UPDATE persons
                SET {}_date = {}
                WHERE person_id = {}"""

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
        cur.execute(sql.format(event_type, date, person_id))
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

def update_place(person_id, event_type, place):
    """
    Update a place value in a person

    Args:
        (integer) person_id - Person ID
        (string) event_type - Type of event matching with a column (birth etc.)
        (string) place - Name of place
    Returns:
        (int) updated_rows - How many rows updated
    """

    sql = """ UPDATE persons
                SET {}_place = {}
                WHERE person_id = {}"""

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
        cur.execute(sql.format(event_type, place, person_id))
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

def update_number_of_children(person_id, number_of_children):
    """
    Update number of children in a person

    Args:
        (integer) person_id - Person ID
        (integer) number_of_children - Number of known children
    Returns:
        (int) updated_rows - How many rows updated
    """

    sql = """ UPDATE persons
                SET number_of_children = {}
                WHERE person_id = {}"""

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
        cur.execute(sql.format(number_of_children, person_id))
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

def update_comments(person_id, comments):
    """
    Update a comment value in a person

    Args:
        (integer) person_id - Person ID
        (string) comments - Comments about the person
    Returns:
        (int) updated_rows - How many rows updated
    """

    sql = """ UPDATE persons
                SET comments = {}
                WHERE person_id = {}"""

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
        cur.execute(sql.format(comments, person_id))
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


def get_person(person_id):
    """
    Get and display a person from database

    Args:
        (integer) person_id - Person ID
    """

    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT * FROM persons WHERE person_id = {}".format(person_id))
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

def add_person(page_number):
    """ Add a person """

    print('Add a new person in database:')

    # MAKE A PERSON AS AN OBJECT
    first_names = input('- First names: ')
    last_name = input('- Last name: ')

    birth_date = input('- Birth date: ') # different date formats
    birth_place = input('- Birth place: ')
    death_date = input('- Death date: ')
    death_place = input('- Death place: ')
    comments = input('- Additional comments: ')

    # Checks and adds user to database
    person_id = initialize_person(page_number)
    update_names(person_id, first_names, last_name)

    update_date(person_id, 'birth', convert_date_dmy_to_ymd(birth_date))
    update_place(person_id, 'birth', birth_place)

    update_date(person_id, 'death', convert_date_dmy_to_ymd(death_date))
    update_place(person_id, 'death', death_place)

    update_comments(person_id, comments)

    get_person(person_id)

def main():
    """ Main function """

    page_number = None
    add_more_persons = True
    while add_more_persons:
        if not page_number:
            page_number = input('Provide page number: ')
        else:
            page_number_new = input('Provide page number (default {}): '.format(page_number))
            if len(page_number_new) != 0:
                page_number = page_number_new
        # CHECK IF PAGE IS REALLY INT

        add_person(page_number)

if __name__ == "__main__":
    main()
