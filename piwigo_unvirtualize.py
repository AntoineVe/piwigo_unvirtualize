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

__docformat__ = 'restructuredtext en'

def db_query(db_infos, query):
    result = []
    cnx = mysql.connector.connect(
            user=db_infos[0],
            password=db_infos[1],
            host=db_infos[2],
            database=db_infos[3]
            )
    cur = cnx.cursor()
    cur.execute(query)
    for item in cur:
        result.append(item)
    cnx.close()
    return(result)

#def get_photo_list(db_infos):

