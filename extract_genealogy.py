import psycopg2
from config import config

def initialize_database_row(id_name, column_names, column_values, table_name):
    """
    Adds a row in given table with initial data

    Args:
        (string list) column_names - Column names
        (integer list) column_values - Column values
        (string) table_name - Table name
    Returns:
        (int) id_number - ID number
    """

    # Create strings for added column data
    column_list = None
    value_list = None
    first_column = True
    for column_name, column_value in zip(column_names, column_values):
        if column_value is None:
            column_value = 'NULL' # Changing to SQL-supported type

        if first_column:
            column_list = column_name
            value_list = str(column_value)
            first_column = False
        else:
            column_list = column_list + ', ' + column_name
            value_list = value_list + ', ' + str(column_value)

    sql = 'INSERT INTO {} ({}) VALUES({}) RETURNING {};'.format(table_name, column_list,
                                                                value_list, id_name)

    conn = None
    id_number = None
    try:
        # read database configuration
        params = config()
        # connect to the PostgreSQL database
        conn = psycopg2.connect(**params)
        # create a new cursor
        cur = conn.cursor()
        # execute the INSERT statement
        cur.execute(sql)
        # get the generated ID back
        id_number = cur.fetchone()[0]
        # commit the changes to the database
        conn.commit()
        # close communication with the database
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return id_number


def initialize_person(page_number):
    """
    Inserts a person into database

    Args:
        (integer) page - Page number
    Returns:
        (int) person_id - Person ID
    """

    column_names = ['page_number']
    column_values = [page_number]

    person_id = initialize_database_row('person_id', column_names,
                                        column_values, 'persons')

    return person_id


def modify_person(person_id, column_names, column_values):
    """
    Adds or modifies person data

    Args:
        (integer) person_id - Person's ID
        (list) column_names - Names of columns
        (list) column_values - Values of columns
    Returns:
        (int) updated_rows - How many rows updated
    """

    sql = "UPDATE persons SET "

    # Supported column names and types
    integer_columns = ['page_number', 'page_from', 'page_to']
    boolean_columns = ['deceased']
    string_columns = ['first_names', 'last_name', 'birth_date',
                      'birth_place', 'death_date', 'death_place',
                      'comments', 'gender']

    first_column = True
    for column_name, column_value in zip(column_names, column_values):

        # SET list separated by commas
        if not first_column:
            sql = sql + ', '

        # Add columns to SQL command by type
        if column_name in integer_columns:
            if column_value is None:
                column_value = 'NULL' # Changing to SQL-supported type
            sql = sql + '{} = {}'.format(column_name, column_value)

        elif column_name in boolean_columns:
            sql = sql + '{} = {}'.format(column_name, column_value)

        elif column_name in string_columns:
            if len(column_value) == 0:
                column_value = 'NULL' # Empty strings should be NULL
            else:
                # Change ' characters with '' for SQL input compatibility
                if column_value.find('\'') != -1:
                    column_value.replace('\'', '\'\'')

                column_value = "'" + column_value + "'" # Strings within '' in SQL

            sql = sql + '{} = {}'.format(column_name, column_value)
        else:
            print("ERROR: Unsupported column name '{}'".format(column_name))

        if first_column:
            first_column = False

    sql = sql + ' WHERE person_id = {}'.format(person_id)

    # Save values to PostgreSQL database
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
        cur.execute(sql)
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
            date = date_parts[1] + '-' + date_parts[0] + '-XX'
        elif len(date_parts) == 1:
            date = date_parts[0] + '-XX-XX'
        else:
            print('Not a valid date: {}. Date not converted.'.format(date))
    return date


def get_database_row(id_name, id_value, table_name):
    """
    Get a row from database by ID number

    Args:
        (string) id_name - Name if ID column
        (integer) id_value - ID number
        (string) table_name - Name of table
    Returns:
        (tuple) person_data - Personal data
    """

    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("SELECT * FROM {} WHERE {} = {}".format(table_name, id_name, id_value))

        values = cur.fetchone() # Values as tuple
        columns = [desc[0] for desc in cur.description] # columns as list

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

    return columns, values


def get_person(person_id, print_values=False):
    """
    Get personal data saved in database

    Args:
        (integer) person_id - Person ID
    Returns:
        (list) columns - Data columns
        (tuple) values - Data values
    """

    columns, values = get_database_row('person_id', person_id, 'persons')

    # Optionally print saved values
    if print_values:
        print('Person values in database:')
        for column, value in zip(columns, values):
            print('"{}": "{}"'.format(column, value))

    return columns, values


def get_relationship(relationship_id, print_values=False):
    """
    Get relationship data saved in database

    Args:
        (integer) relationship_id - Relationship ID
    Returns:
        (list) columns - Data columns
        (tuple) values - Data values
    """

    columns, values = get_database_row('relationship_id', relationship_id, 'relationships')

    # Optionally print saved values
    if print_values:
        print('Relationship values in database:')
        for column, value in zip(columns, values):
            print('"{}": "{}"'.format(column, value))

    return columns, values


def get_child(child_id, print_values=False):
    """
    Get child data saved in database

    Args:
        (integer) child_id - Child ID
    Returns:
        (list) columns - Data columns
        (tuple) values - Data values
    """

    columns, values = get_database_row('child_id', child_id, 'children')

    # Optionally print saved values
    if print_values:
        print('Child values in database:')
        for column, value in zip(columns, values):
            print('"{}": "{}"'.format(column, value))

    return columns, values


def add_person(page_number):
    """
    Inputs person data and adds person to database

    Args:
        (integer) page number - Page number
    Returns:
        (integer) person_id - Saved Person ID
    """

    print('Add a new person in database:')

    first_names = None
    last_name = None
    gender = None
    birth_date = None
    birth_place = None
    death_date = None
    death_place = None
    deceased = None
    page_from = None
    page_to = None
    comments = None


    review_finished = False
    while not review_finished:

        first_names = input('- First names: ').strip()
        last_name = input('- Last name: ').strip()
        gender = input('- Gender: ').strip().lower()

        if gender in ('m', 'male'):
            gender = 'MALE'
        elif gender in ('f', 'female'):
            gender = 'FEMALE'

        birth_date = input('- Birth date: ').strip() # different date formats
        birth_place = input('- Birth place: ').strip()
        death_date = input('- Death date: ').strip()
        death_place = input('- Death place: ').strip()

        birth_date = convert_date_dmy_to_ymd(birth_date)
        death_date = convert_date_dmy_to_ymd(death_date)

        # Process deceased
        deceased = None # reset value if values changed
        # - If person died or born over 101 years ago, we can assume deceased
        if len(death_date) != 0:
            deceased = True

        if birth_date != 0:
            try:
                birth_year = int(birth_date[0:4])
            except ValueError:
                pass
            else:
                if birth_year <= 1919:
                    deceased = True

        # - Otherwise ask it from user
        while deceased is None:
            deceased_input = input('- Person deceased (y/n): ').strip().lower()
            if deceased_input in ('y', 'yes'):
                deceased = True
            elif deceased_input in ('n', 'no'):
                deceased = False
            else:
                print('ERROR: Please, answer y(es) or n(o).')

        # Add from and to page references
        reference_input = input('Add page references (y/N)? ').strip().lower()
        if reference_input in ('y', 'yes'):
            page_from = input_integer('  - Person comes from page: ', True)
            page_to = input_integer('  - Person goes to page: ', True)

        comments = input('- Additional comments: ').strip()

        print('\nReview input for person:')
        print('- First names: {}'.format(first_names))
        print('- Last name: {}'.format(last_name))
        print('- Gender: {}'.format(gender))
        print('- Birth date: {}'.format(birth_date))
        print('- Birth place: {}'.format(birth_place))
        print('- Death date: {}'.format(death_date))
        print('- Death place: {}'.format(death_place))
        print('- Person deceased: {}'.format(deceased))
        if reference_input in ('y', 'yes'):
            print('- Page from: {}'.format(page_from))
            print('- Page to: {}'.format(page_to))
        print('- Comments about person: {}'.format(comments))

        valid_input = False
        while not valid_input:
            validation_input = input('Everything looks correct (y/n)? ').strip().lower()
            if validation_input in ('y', 'yes'):
                review_finished = True
                valid_input = True
            elif validation_input in ('n', 'no'):
                print('Asking marriage information again.')
                valid_input = True
            else:
                print('ERROR: Please answer y(es) or n(o).')

    # Checks and adds user to database
    person_id = initialize_person(page_number)

    # Add other person information
    column_names = ['first_names', 'last_name', 'birth_date', 'birth_place',
                    'death_date', 'death_place', 'comments', 'gender',
                    'deceased', 'page_from', 'page_to']
    column_values = [first_names, last_name, birth_date, birth_place,
                     death_date, death_place, comments, gender,
                     deceased, page_from, page_to]
    modify_person(person_id, column_names, column_values)

    # Print saved data
    get_person(person_id, print_values=True)

    return person_id


def add_relationship(partner1_id, partner2_id=None):
    """
    Inputs relationship data and adds a relationshiup to database

    Args:
        (integer) partner1_id - Partner 1 ID
        (integer) partner2_id - Partner 2 ID (optional, 'None' if not known)
    Returns:
        (integer) relationship_id - Saved Relationship ID
    """

    print('Adding a relationship')

    relationship_marriage = None
    marriage_date = None
    marriage_place = None
    divorce_date = None
    divorce_place = None
    comments = None

    review_finished = False
    while not review_finished:

        relationship_marriage = input('- Add marriage information (Y/n)?: ').strip().lower()

        if relationship_marriage not in ('n', 'no'):
            marriage_date = input('- Married date: ').strip()
            marriage_place = input('- Married place: ').strip()
            divorce_date = input('- Divorce date: ').strip()
            divorce_place = input('- Divorce place: ').strip()

        comments = input('- Comments about relationship: ').strip()

        print('\nReview input for relationship:')
        print('- Partner 1: {}'.format(print_person(partner1_id)))
        if partner2_id is not None:
            print('- Partner 2: {}'.format(print_person(partner2_id)))
        else:
            print('- Partner 2: [NK]')
        if relationship_marriage not in ('n', 'N'):
            print('- Marriage date: {}'.format(marriage_date))
            print('- Marriage place: {}'.format(marriage_place))
            print('- Divorce date: {}'.format(divorce_date))
            print('- Divorce place: {}'.format(divorce_place))

        print('- Comments about relationship: {}'.format(comments))

        valid_input = False
        while not valid_input:
            validation_input = input('Everything looks correct (y/n)? ').strip().lower()
            if validation_input in ('y', 'yes'):
                review_finished = True
                valid_input = True
            elif validation_input in ('n', 'no'):
                print('Asking marriage information again.')
                valid_input = True
            else:
                print('Please type y(es) or n(o).')

    relationship_id = initialize_relationship(partner1_id, partner2_id)

    if relationship_marriage not in ('n', 'N'):
        marriage_date = convert_date_dmy_to_ymd(marriage_date)
        divorce_date = convert_date_dmy_to_ymd(divorce_date)

    column_names = ['marriage_date', 'marriage_place', 'divorce_date',
                    'divorce_place', 'comments']
    column_values = [marriage_date, marriage_place, divorce_date,
                     divorce_place, comments]
    modify_relationship(relationship_id, column_names, column_values)

    # Print saved data
    get_relationship(relationship_id, print_values=True)

    return relationship_id


def initialize_relationship(partner1_id, partner2_id):
    """
    Inserts a relationship into database

    Args:
        (integer) partner1_id - Person ID for partner 1
        (integer) partner2_id - Person ID for partner 2 ('None' if not known)
    Returns:
        (int) relationship_id - Saved Relationship ID
    """

    column_names = ['person_id_partner1', 'person_id_partner2']
    column_values = [partner1_id, partner2_id]

    relationship_id = initialize_database_row('relationship_id', column_names,
                                              column_values, 'relationships')

    return relationship_id


def modify_relationship(relationship_id, column_names, column_values):
    """
    Adds or modifies relationship data

    Args:
        (integer) relatinship_id - Relationship ID
        (list) column_names - Names of columns
        (list) column_values - Values of columns
    Returns:
        (int) updated_rows - How many rows updated
    """

    sql = "UPDATE relationships SET "

    # Supported column names and types
    integer_columns = ['person_id_partner1', 'person_id_partner2']
    string_columns = ['marriage_date', 'marriage_place', 'divorce_date',
                      'divorce_place', 'comments']

    first_column = True
    for column_name, column_value in zip(column_names, column_values):

        # SET list separated by commas
        if not first_column:
            sql = sql + ', '

        # Add columns to SQL command by type
        if column_name in integer_columns:
            if column_value is None:
                column_value = 'NULL' # Changing to SQL-supported type
            sql = sql + '{} = {}'.format(column_name, column_value)

        elif column_name in string_columns:
            if column_value is None:
                column_value = 'NULL' # Changing to SQL-supported type
            elif len(column_value) == 0:
                column_value = 'NULL' # Empty strings should be NULL
            else:
                # Change ' characters with '' for SQL input compatibility
                if column_value.find('\'') != -1:
                    column_value.replace('\'', '\'\'')

                column_value = "'" + column_value + "'" # Strings within '' in SQL

            sql = sql + '{} = {}'.format(column_name, column_value)
        else:
            print("ERROR: Unsupported column name '{}'".format(column_name))

        if first_column:
            first_column = False

    sql = sql + ' WHERE relationship_id = {}'.format(relationship_id)

    # Save values to PostgreSQL database
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
        cur.execute(sql)
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


def add_child(relationship_id, person_id, verbose=False):
    """
    Inputs child data and adds a child to database

    Args:
        (integer) relationship_id - Relationship ID in which the child is added
        (integer) person_id - Person ID of the person who is added as a child
        (boolean) verbose - Enable/disable a verbose mode (disabled by default)
    Returns:
        (integer) child_id - Saved Child ID
    """

    relationship_provided = None
    if relationship_id:
        relationship_provided = True
        if verbose:
            # Change ID to name
            print('Adding a child to relationship ID: {}'.format(relationship_id))
    else:
        relationship_provided = False

    child_provided = None
    if person_id:
        child_provided = True
        if verbose:
            # Change ID to name
            print('Adding person ID as a child: {}'.format(person_id))
    else:
        child_provided = False

    review_finished = False

    # No review needed if information already provided
    if relationship_provided and child_provided:
        review_finished = True

    # Read and review input
    while not review_finished:
        if not relationship_provided:
            relationship_id = input('- Relationship ID: ').strip()

        if not child_provided:
            person_id = input('- Child ID: ').strip()

        print('Review input:')
        print('- Relationship ID: {}'.format(relationship_id))
        print('- Child ID: {}'.format(person_id))

        ok_to_proceed = input('Everything looks correct (Y/n)?').strip().lower()
        if ok_to_proceed not in ('n', 'no'):
            review_finished = True

    child_id = initialize_child(relationship_id, person_id)

    # Print saved data
    get_child(child_id, print_values=True)

    return child_id


def initialize_child(relationship_id, person_id):
    """
    Inserts a child into database

    Args:
        (integer) relationship_id - Relationship ID that the child belongs to
        (integer) person_id - Person ID for the child
    Returns:
        (int) child_id - Saved Child ID
    """

    column_names = ['relationship_id', 'person_id']
    column_values = [relationship_id, person_id]

    child_id = initialize_database_row('child_id', column_names,
                                       column_values, 'children')

    return child_id


def add_family(person_id_head, page_number):
    """
    Adds a family line recursively

    Args:
        (integer) person_id_head - Person ID of head person in family line
        (integer) page_number - Page number
    """

    print('Adding a family')

    add_more_spouses = True
    while add_more_spouses:
        spouse_known = input('Is the spouse known (Y/n)? ').lower()
        person_id_spouse = None
        if spouse_known not in ('n', 'no'):
            page_number_new = input_integer('Provide page number (default {}): '.format(
                page_number))
            if page_number_new is not None:
                page_number = page_number_new

            person_id_spouse = add_person(page_number)

        relationship_id = add_relationship(person_id_head, person_id_spouse)

        add_more_children = False
        print_relationship(relationship_id)
        input_more_children = input('Add children to this relationship (y/N)? ').lower()
        if input_more_children in ('y', 'yes'):
            add_more_children = True

        while add_more_children:
            page_number_new = input_integer('Provide page number (default {}): '.format(
                page_number))
            if page_number_new is not None:
                page_number = page_number_new

            person_id_child = add_person(page_number)

            add_child(relationship_id, person_id_child, False)

            input_family = input('Add family for {} (y/N)? '.format(
                print_person(person_id_child))).lower()
            if input_family in ('y', 'yes'):
                add_family(person_id_child, page_number)

            print_relationship(relationship_id)
            input_more_children = input('Add more children to this relationship (Y/n)? ').lower()
            if input_more_children in ('n', 'no'):
                add_more_children = False

        input_more_spouses = input('Add more spouses for {} (y/N)? '.format(
            print_person(person_id_head))).lower()
        if input_more_spouses not in ('y', 'yes'):
            add_more_spouses = False


def input_integer(input_message, allow_empty=True, allow_zero=False):
    """
    Inputs a valid integer input

    Args:
        (string) input_message - A message printed before input
        (integer) allow_empty - Allow empty input (enabled by default)
        (integer) allow_zero - Allow zero as input (disabled by default)
    Returns:
        (string/integer/none) read_input - Input read
    """

    valid_input = False
    while not valid_input:
        read_input = input(input_message).strip()

        if len(read_input) != 0:
            try:
                read_input = int(read_input)
            except ValueError:
                print('ERROR: Please, provide an integer value.')
            else:
                if read_input > 0:
                    valid_input = True
                elif allow_zero and read_input == 0:
                    valid_input = True
                else:
                    print('ERROR: Please, provide value larger than zero.')
        else:
            if allow_empty:
                read_input = None
                valid_input = True
            else:
                print('ERROR: Please, provide a non-empty value.')

    return read_input


def print_person(person_id):
    """
    Prepares a person data print

    Args:
        (integer) person_id - Person ID
    Returns:
        (string) print_data - Prepared print data
    """

    person_columns, person_data = get_person(person_id)

    first_names = person_data[2]
    last_name = person_data[3]
    birth_date = person_data[4]
    death_date = person_data[6]


    if not first_names:
        first_names = '[NK]'
    if not last_name:
        last_name = '[NK]'

    if birth_date:
        if birth_date[4:] == '-XX-XX': # month and day missing
            birth_date = birth_date[0:4]
        elif birth_date[7:] == '-XX': # only day missing
            birth_date = birth_date[0:7]

    if death_date:
        if death_date[4:] == '-XX-XX': # month and day missing
            death_date = death_date[0:4]
        elif death_date[7:] == '-XX': # only day missing
            death_date = death_date[0:7]

    print_data = None
    if birth_date and death_date:
        print_data = '{} {} (b. {} d. {})'.format(first_names, last_name, birth_date, death_date)
    elif birth_date and not death_date:
        print_data = '{} {} (b. {})'.format(first_names, last_name, birth_date)
    elif not birth_date and death_date:
        print_data = '{} {} (d. {})'.format(first_names, last_name, death_date)
    else:
        print_data = '{} {}'.format(first_names, last_name)

    return print_data


def print_relationship(relationship_id):
    """
    Prepares a relationship data print

    Args:
        (integer) relationship_id - Relationship ID
    """

    print('\nRelationship:')

    # Read relationship data
    relationship_columns, relationship_data = get_relationship(relationship_id)

    person_id_partner1 = relationship_data[1]
    person_id_partner2 = relationship_data[2]
    marriage_date = relationship_data[3]
    divorce_date = relationship_data[5]

    # Acquire and process person data
    partner1_print = None
    if person_id_partner1:
        partner1_print = print_person(person_id_partner1)
        print('- Partner 1: {}'.format(partner1_print))
    else:
        print('- Partner 1: [NK]')

    partner2_print = None
    if person_id_partner2:
        partner2_print = print_person(person_id_partner2)
        print('- Partner 2: {}'.format(partner2_print))
    else:
        print('- Partner 2: [NK]')

    # Process marriage dates
    if marriage_date:
        if marriage_date[4:] == '-XX-XX': # month and day missing
            marriage_date = marriage_date[0:4]
        elif marriage_date[7:] == '-XX': # only day missing
            marriage_date = marriage_date[0:7]
    if divorce_date:
        if divorce_date[4:] == '-XX-XX': # month and day missing
            divorce_date = divorce_date[0:4]
        elif divorce_date[7:] == '-XX': # only day missing
            divorce_date = divorce_date[0:7]

    if marriage_date and divorce_date:
        print('- Marriage: m. {} div. {}'.format(marriage_date, divorce_date))
    elif marriage_date and not divorce_date:
        print('- Marriage: m. {}'.format(marriage_date))
    elif not marriage_date and divorce_date:
        print('- Marriagew: div. {}'.format(divorce_date))


def main():
    """ Main function """

    add_type = input('Add (p)person, (r)elationship or (c)hild? ').lower()

    # Add a person or a whole family line
    if add_type in ('p', 'person'):
        page_number = None
        add_more_persons = True
        while add_more_persons:
            if not page_number:
                page_number = input_integer('Provide page number: ', False)
            else:
                page_number_new = input_integer('Provide page number (default {}): '.format(
                    page_number))
                if page_number_new is not None:
                    page_number = page_number_new

            person_id = add_person(page_number)

            input_family = input('Add family for {} (Y/n)? '.format(
                print_person(person_id))).lower()
            if input_family.lower() not in ('n', 'no'):
                add_family(person_id, page_number)

            input_more_persons = input('Add more persons (Y/n)? ').lower()
            if input_more_persons in ('n', 'no'):
                add_more_persons = False

    # Add manually a relationship by IDs
    elif add_type in ('r', 'relationship'):
        add_more_relationships = True
        while add_more_relationships:
            person_id_head = input_integer('Provide ID for partner 1: ')

            spouse_known = input('Is the spouse known (Y/n)? ').lower()
            person_id_spouse = None
            if spouse_known not in ('n', 'no'):
                person_id_spouse = input_integer('Provide ID for partner 2: ')

            add_relationship(person_id_head, person_id_spouse)

            input_more_relationships = input('Add more relationships (Y/n)? ').lower()
            if input_more_relationships in ('n', 'no'):
                add_more_relationships = False

    # Add manually a child by IDs
    elif add_type in ('c', 'child'):

        relationship_id = input('Provide a relationship ID: ').strip()

        add_more_persons = True
        while add_more_persons:
            add_child(relationship_id, None)

            input_more_children = input('Add more children (Y/n)?').lower()
            if input_more_children in ('n', 'no'):
                add_more_persons = False

    else:
        print('Unknown entry')

if __name__ == "__main__":
    main()
