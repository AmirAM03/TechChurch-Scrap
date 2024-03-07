# This module developed specifically for interaction with Data Base
# and able to create, modify, transfer ,etc DB data records

import traceback
import sqlite3
import sys


def setup_table_in_db():  # Setup new DB table in proven file with proven structure
    connection = sqlite3.connect("cached.db")
    #  print(connection.total_changes)
    cursor = connection.cursor()
    cursor.execute("CREATE TABLE magazines (title TEXT, author TEXT, category TEXT, tags TEXT, "
                   "date TEXT, link TEXT)")
    connection.close()


def fetch_db_column(column):  # Get all rows of a certain DB column
    connection = sqlite3.connect("cached.db")
    cursor = connection.cursor()
    resp = cursor.execute(f"SELECT {column} FROM magazines").fetchall()
    connection.close()
    return resp


def insert_magazine_records_to_db(magazines_list):
    # You should pass the complete json object that you catch from tech crunch end point to this function
    connection = sqlite3.connect("cached.db")
    with connection:
        cursor = connection.cursor()
        for record in magazines_list:
            tmp = record["yoast_head_json"]
            try:
                cursor.execute(f"INSERT INTO magazines "
                               f"(title, author, category, tags, date, link) "
                               f"VALUES (\"{tmp['title']}\", \"{tmp['author']}\","
                               f" \"{tmp['schema']['@graph'][0]['articleSection']}\", "
                               f"\"{tmp["schema"]["@graph"][0]['keywords'] if 'keywords' in tmp["schema"]["@graph"][0].keys() else ''}\","
                               f" \"{record['date']}\", \"{record['link']}\");")
                connection.commit()
            except:
                traceback.print_exc()
                sys.exit()
                print("Special data returned from tech crunch. Can't be inputted in our DB due to empty fields")
                print(tmp["schema"]["@graph"][0])


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
