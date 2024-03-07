# This module developed specifically for interaction with Data Base
# and able to create, modify, transfer ,etc DB data records


import sqlite3


def setup_table_in_db():
    connection = sqlite3.connect("cached.db")
    #  print(connection.total_changes)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE magazines (search_term TEXT, author TEXT, category TEXT, tags TEXT, "
                   "date TEXT, link TEXT)")
    connection.close()


def fetch_db_column(column):  # Get all record of a certain DB column
    connection = sqlite3.connect("cached.db")
    cursor = connection.cursor()
    resp = cursor.execute(f"SELECT {column} FROM magazines").fetchall()
    connection.close()
    return resp


def insert_record_list_to_db(records):
    connection = sqlite3.connect("cached.db")
    with connection:
        cursor = connection.cursor()
        for record in records:
            cursor.execute(f"INSERT INTO magazines "
                           f"(fetched_term, author, title, publisher, "
                           f"year, pages_count, language, size, extension, link1, link2) "
                           f"VALUES (\"{record['fetched_term']}\", \"{record['author']}\","
                           f" \"{record['title']}\", \"{record['publisher']}\","
                           f" \"{record['year']}\", \"{record['pages_count']}\", \"{record['language']}\", "
                           f"\"{record['size']}\", \"{record['extension']}\","
                           f" \"{record['link1']}\", \"{record['link2']}\");")
        connection.commit()


def fetch_db_record_using_certain_value_at_certain_column(column_name, column_value):
    # Get record with certain value at certain columns
    connection = sqlite3.connect("cached.db")
    with connection:
        cursor = connection.cursor()
        resp = cursor.execute(f"SELECT * FROM magazines WHERE {column_name} = \"{column_value}\";").fetchall()
        return resp


def clean_db_table(table_name):  # Takes DB Table name and clear all records(Rows) of relevant table
    connection = sqlite3.connect("cached.db")
    with connection:
        cursor = connection.cursor()
        cursor.execute(f'DELETE FROM {table_name};')
        connection.commit()


def delete_relevant_term_records_from_db(column_name, column_value):
    # Delete records with certain value at certain column
    connection = sqlite3.connect("cached.db")
    with connection:
        cursor = connection.cursor()
        cursor.execute(f'DELETE FROM magazines WHERE {column_name} = \"{column_value}\";')
        connection.commit()

