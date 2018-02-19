"""

Uses sqlalchemy and MySQL to store lists of URLs still to be crawled and to fetch them later.
Customize for your needs/database system.

"""

import sqlalchemy
import json
import pymysql

def storeinDB(crawllist):
    """
    Store a list of URLs into the database for future use.

    :param crawllist:
    :return: none, stores in database

    """
    stringlist = json.dumps(crawllist)

    engine = sqlalchemy.create_engine("mysql+pymysql://") #Fill in your MySQL database connection information

    sql = "INSERT INTO your.table (indices) VALUES ('%s')" % (stringlist) #Customize for your database.

    engine.execute(sql)
    return print("It's in the database! Go forth my henchman!")


def fetchlist():
    """
    Fetch the last INSERT from the database.
    Be sure the fetched list is the intended list by ensuring the last list put in the database is
    the one desired.
    :return: list of URLs

    """
    engine = sqlalchemy.create_engine("mysql+pymysql://") #Fill in your MySQL database connection information

    sql = "SELECT encoded FROM sys.psle_links" #Customize for your database
    query = engine.execute(sql)
    result = query.fetchall()

    real = json.loads(result[-1][0]) #Customize here to fetch a list that is not the last INSERT.
    return real
