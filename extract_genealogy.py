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

def update_date(value_id, event_type, date):
    """
    Update a date value in a person or relationship

    Args:
        (integer) value_id - Person or relationship ID
        (string) event_type - Type of event matching with a column (birth etc.)
        (string) date - Date in "YYYY-MM-DD" format
    Returns:
        (int) updated_rows - How many rows updated
    """

    sql = None
    if event_type in ('birth', 'death'):
        sql = """ UPDATE persons
                    SET {}_date = {}
                    WHERE person_id = {}"""
    elif event_type in ('marriage', 'divorce'):
        sql = """ UPDATE relationships
                    SET {}_date = {}
                    WHERE relationship_id = {}"""

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
        cur.execute(sql.format(event_type, date, value_id))
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

def update_place(value_id, event_type, place):
    """
    Update a place value in a person or relationship

    Args:
        (integer) id - Person or relationship ID
        (string) event_type - Type of event matching with a column (birth etc.)
        (string) place - Name of place
    Returns:
        (int) updated_rows - How many rows updated
    """

    sql = None
    if event_type in ('birth', 'death'):
        sql = """ UPDATE persons
                    SET {}_place = {}
                    WHERE person_id = {}"""
    elif event_type in ('marriage', 'divorce'):
        sql = """ UPDATE relationships
                    SET {}_place = {}
                    WHERE relationship_id = {}"""

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
        cur.execute(sql.format(event_type, place, value_id))
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

def update_comments(value_id, comment_type, comments):
    """
    Update a comment value in a person

    Args:
        (integer) value_id - Person or relationship ID
        (string) comment_type - 'person' or 'relationship'
        (string) comments - Comments about the person or relationship
    Returns:
        (int) updated_rows - How many rows updated
    """

    sql = None
    if comment_type == 'person':
        sql = """ UPDATE persons
                    SET comments = {}
                    WHERE person_id = {}"""
    elif comment_type == 'relationship':
        sql = """ UPDATE relationships
                    SET comments = {}
                    WHERE relationship_id = {}"""

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
        cur.execute(sql.format(comments, value_id))
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

    update_comments(person_id, 'person', comments)

    get_person(person_id)

    return person_id


def add_relationship(partner1_id, partner2_id):
    """ Add a relationship """

    # Change partner2 optional

    partner1_provided = None
    if partner1_id:
        partner1_provided = True
        print('Adding a relationship for {}'.format(partner1_id))
    else:
        partner1_provided = False

    partner2_provided = None
    if partner2_id:
        partner2_provided = True
        print('Adding a relationship for {}'.format(partner2_id))
    else:
        partner2_provided = False

    relationship_marriage = None
    marriage_date = None
    marriage_place = None
    divorce_date = None
    divorce_place = None
    comments = None

    review_finished = True
    while review_finished:

        if not partner1_provided:
            partner1_id = input('- Partner 1 ID: ')

        if not partner2_provided:
            partner2_id = input('- Partner 2 ID (if known): ')

            try:
                partner2_id += 1
            except TypeError:
                partner2_id = None

        relationship_marriage = input('- Married (Y/n)?: ')

        if relationship_marriage not in ('n', 'N'):
            marriage_date = input('- Married date: ')
            marriage_place = input('- Married place: ')
            divorce_date = input('- Divorce date: ')
            divorce_place = input('- Divorce place: ')

        comments = input('- Comments about relationship: ')

        print('Review input:')
        print('- Partner 1 ID: {}'.format(partner1_id))
        print('- Partner 2 ID: {}'.format(partner2_id))
        # print('- Married: {}'. format(relationship_marriage))
        if relationship_marriage not in ('n', 'N'):
            print('- Marriage date: {}'.format(marriage_date))
            print('- Marriage place: {}'.format(marriage_place))
            print('- Divorce date: {}'.format(divorce_date))
            print('- Divorce place: {}'.format(divorce_place))

        print('- Comments about relationship: {}'.format(comments))

        ok_to_proceed = input('Everything looks correct (Y/n)?')
        if ok_to_proceed not in ('n', 'N'):
            review_finished = False

    relationship_id = initialize_relationship(partner1_id, partner2_id)

    if relationship_marriage not in ('n', 'N'):
        update_date(relationship_id, 'marriage', convert_date_dmy_to_ymd(marriage_date))
        update_place(relationship_id, 'marriage', marriage_place)
        update_date(relationship_id, 'divorce', convert_date_dmy_to_ymd(divorce_date))
        update_place(relationship_id, 'divorce', divorce_place)

    update_comments(relationship_id, 'relationship', comments)

    return relationship_id


def initialize_relationship(partner1_id, partner2_id):
    """
    Inserts a relationship into database

    Args:
        (integer) partner1_id - Person ID for partner 1
        (integer) partner2_id - Person ID for partner 2 ('None' if not known)
    Returns:
        (int) relationship_id - Relationship ID
    """

    sql = """INSERT INTO relationships(person_id_partner1, person_id_partner2) VALUES({}, {})
          RETURNING relationship_id;"""

    if partner2_id is None:
        partner2_id = 'NULL'

    conn = None
    relationship_id = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql.format(partner1_id, partner2_id))
        # get the generated UID back
        relationship_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return relationship_id

def add_child(relationship_id, person_id):
    """ Add a child """

    relationship_provided = None
    if relationship_id:
        relationship_provided = True
        print('Adding a child to relationship ID: {}'.format(relationship_id))
    else:
        relationship_provided = False

    child_provided = None
    if person_id:
        child_provided = True
        print('Adding person ID as a child: {}'.format(person_id))
    else:
        child_provided = False

    review_finished = True
    while review_finished:

        if not relationship_provided:
            relationship_id = input('- Relationship ID: ')

        if not child_provided:
            person_id = input('- Child ID: ')

        print('Review input:')
        print('- Relationship ID: {}'.format(relationship_id))
        print('- Child ID: {}'.format(person_id))

        ok_to_proceed = input('Everything looks correct (Y/n)?')
        if ok_to_proceed not in ('n', 'N'):
            review_finished = False

    initialize_child(relationship_id, person_id)

def initialize_child(relationship_id, person_id):
    """
    Inserts a child into database

    Args:
        (integer) relationship_id - Relationship ID that the child belongs to
        (integer) person_id - Person ID for the child
    Returns:
        (int) child_id - Child ID
    """

    sql = """INSERT INTO children(relationship_id, person_id) VALUES({}, {})
          RETURNING child_id;"""

    conn = None
    child_id = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql.format(relationship_id, person_id))
        # get the generated UID back
        child_id = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return child_id


def add_family(person_id_head, page_number):
    """  Adds a family """

    print('Adding a relationship')

    add_more_spouses = True
    while add_more_spouses:
        spouse_known = input('Is the spouse known (y/n)? ').lower()
        person_id_spouse = None
        if spouse_known not in ('n', 'no'):
            page_number_new = input('Provide page number (default {}): '.format(page_number))
            if len(page_number_new) != 0:
                page_number = page_number_new
                # CHECK IF PAGE IS REALLY INT

            person_id_spouse = add_person(page_number)

        relationship_id = add_relationship(person_id_head, person_id_spouse)

        add_more_children = False
        input_more_children = input('Children from relationship {} (y/n)? '.format(relationship_id)).lower()
        if input_more_children in ('y', 'yes'):
            add_more_children = True

        while add_more_children:
            page_number_new = input('Provide page number (default {}): '.format(page_number))
            if len(page_number_new) != 0:
                page_number = page_number_new
                # CHECK IF PAGE IS REALLY INT

            person_id_child = add_person(page_number)

            add_child(relationship_id, person_id_child)

            input_family = input('Add family for {} (y/N)? '.format(person_id_child)).lower()
            if input_family in ('y', 'yes'):
                add_family(person_id_child, page_number)

            input_more_children = input('Add more children to relationship {} (Y/n)? '.format(relationship_id)).lower()
            if input_more_children in ('n', 'no'):
                add_more_children = False

        input_more_spouses = input('Add more spouses for {} (y/N)? '.format(person_id_head)).lower()
        if input_more_spouses not in ('y', 'yes'):
            add_more_spouses = False


def main():
    """ Main function """

    # Ask to add or modify

    # Ask to add information

    add_type = input('Add (p)person, (r)elationship or (c)hild? ').lower()

    if add_type in ('p', 'person'):
        page_number = None
        add_more_persons = True
        while add_more_persons:
            if not page_number:
                page_number = input('Provide page number: ')
                # CHECK IF PAGE IS REALLY INT
            else:
                page_number_new = input('Provide page number (default {}): '.format(page_number))
                if len(page_number_new) != 0:
                    page_number = page_number_new
                    # CHECK IF PAGE IS REALLY INT

            person_id = add_person(page_number)

            input_family = input('Add family for {} (Y/n)? ').lower()
            if input_family.lower() not in ('n', 'no'):
                add_family(person_id, page_number)

            input_more_persons = input('Add more persons (Y/n)? ').lower()
            if input_more_persons in ('n', 'no'):
                add_more_persons = False

    elif add_type in ('r', 'relationship'):
        add_relationship(None, None)

    elif add_type in ('c', 'child'):

        relationship_id = input('Provide a relationship ID: ')

        add_more_persons = True
        while add_more_persons:
            add_child(relationship_id, None)

            input_more_children = input('Add more children (Y/n)?')
            if input_more_children in ('n', 'N'):
                add_more_persons = False

    else:
        print('Unknown entry')

if __name__ == "__main__":
    main()
