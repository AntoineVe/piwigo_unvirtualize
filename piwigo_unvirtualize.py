#!/bin/env python3
# -*- coding: utf-8 -*-

'''
This script recreate a 'gallery' folder and put all pictures in the correct
folder by reading the piwigo database. Be aware than it creates a 'flat
structure' : no complex subdirectories, one folder is one album. Maybe you will
have duplicates pictures, because they were in multiple categories.
'''

import argparse
import logging
import os
from sys import exit
import shutil

try:
    import mysql.connector
except:
    logging.error("Mysql connector was not loaded. Is it installed ?")
    exit()

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

def get_photo_list(db_infos):
    i = 0
    photos_list = []
    all_pictures = db_query(db_infos, "SELECT `image_id`, `category_id` FROM `piwigo_image_category`")
    logging.info("Creating pictures list (" + str(len(all_pictures)) + " pictures in database)")
    for item in all_pictures:
        category_name = db_query(db_infos, "SELECT `name` FROM `piwigo_categories` WHERE `id` = " + str(item[1]))
        file_info = db_query(db_infos, "SELECT `file`, `path` FROM `piwigo_images` WHERE `id` = " + str(item[0]))
        if file_info != []:
            photos_list.append((category_name[0][0], file_info[0][0].decode(), file_info[0][1]))
        i = i+1
        percent_done = ((i * 100) / int(len(all_pictures)))
        if i % 100 == 0:
            logging.info(str(round(percent_done, 2)) + "% done...")
    return(photos_list)

def create_gallery(photos_list, srvdir, destdir):
    for item in photos_list:
        fromfile = srvdir + item[2][2:]
        tofile = destdir + item[0] + "/" + item[1]
        directory = os.path.dirname(tofile)
        if not os.path.exists(directory):
            os.makedirs(directory)
        try:
            shutil.copy(fromfile, tofile, follow_symlinks=False)
            logging.info("Copied " + fromfile + " to " + tofile)
        except:
            logging.error("/!\ Unable to copy " + fromfile)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('host', action="store", help="MySQL host")
    parser.add_argument('user', action="store", help="MySQL user")
    parser.add_argument('pass', action="store", help="MySQL password")
    parser.add_argument('db', action="store", help="MySQL database")
    parser.add_argument('from', action="store", help="Piwigo upload directory (end with \"/\")")
    parser.add_argument('to', action="store", help="Directory for the new gallery (end with \"/\")")
    parser.add_argument('-v', '--verbose', action="store_true", help="Verbose output")
    args = parser.parse_args()
    settings = vars(args)
    if args.verbose:
        logging.basicConfig(format='[%(asctime)s] %(message)s',level=logging.INFO)
    else:
        logging.basicConfig(format='[%(asctime)s] %(message)s',level=logging.ERROR)
    if settings['from'][-1] != "/":
        logging.error("Please add trailing slash in directory URI")
        exit()
    if settings['to'][-1] != "/":
        logging.error("Please add trailing slash in directory URI")
        exit()
    if not os.path.exists(settings['from']):
        logging.error("Directory " + settings['from'] + " not found !")
        exit()
    if not os.path.exists(settings['to']):
        logging.error("Directory " + settings['to'] + " not found !")
        exit()
    db_infos = (settings['user'], settings['pass'], settings['host'], settings['db'])
    photos_list = get_photo_list(db_infos)
    create_gallery(photos_list, settings['from'], settings['to'])

# vim:set et sts=4 ts=4 tw=80:
