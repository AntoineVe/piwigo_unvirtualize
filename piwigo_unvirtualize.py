#!/bin/env python3
# -*- coding: utf-8 -*-

'''
This script recreate a 'gallery' folder and put all pictures in the correct
folder by reading the piwigo database. Be aware than it creates a 'flat
structure' : no complex subdirectories, one folder is one album.
'''

import argparse
try:
    import mysql.connector
except:
    print("Mysql connector was not loaded. Is it installed ?")

def db_query(dbname, user, password, host, query):
    result = []
    cnx = mysql.connector.connect(
            user=user,
            password=password,
            host=host,
            database=dbname
            )
    cur = cnx.cursor()
    cur.execute(query)
    for item in cur:
        result.append(item)
    cnx.close()
    return(result)

