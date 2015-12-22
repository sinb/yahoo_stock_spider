# -*- coding: utf-8 -*-
"""
Created on Tue Dec 22 10:37:03 2015

@author: hehe
"""
import MySQLdb as mysql
import re
import urllib
from threading import Thread
import json

gmap = {}

def get_login_info(file='config.json'):
    try:
        login_info = json.load(open(file, 'rb'))
        return login_info
    except:
        print "loading config file error"
        return None
        
def login(login_info):
    try:
        connect = mysql.connect(host=login_info['host'], user=login_info['user'], passwd=login_info['password'])
        print "Login succeed"        
        return connect
    except:
        print "Login error, plz check your login info."
        return None
        
def create_db(conn):
    cur = conn.cursor()
    query = 'CREATE DATABASE IF NOT EXISTS stock_data'
    cur.execute(query)
    cur.close()
    
def create_table(conn):
    query = '''
    USE stock_data;
    CREATE TABLE IF NOT EXISTS `stock_price` (
      `symbol` varchar(5) NOT NULL DEFAULT '',
      `last_price` double DEFAULT NULL,
       PRIMARY KEY (`symbol`)
    ) 
    '''
    cur = conn.cursor()
    cur.execute(query)
    cur.close()
    
def get_name(file):
    with open(file, 'rb') as f:
        name_list = f.read()
        name_list = name_list.split()
    return name_list
    
def th(name):
    url = 'http://finance.yahoo.com/q?s=' + name
    regex = '<span id="yfs_l84_' + name.lower() + '">(.+?)</span>'
    pattern = re.compile(regex)
    try:
        htmltext = urllib.urlopen(url).read()
    except:
        print "can't open url"
        return
    results = re.findall(pattern, htmltext)
    try:
        gmap[name] = results[0]
    except:
        "something wrong"
            

def insert_once(gmap, conn):
    for key in gmap:
        print key, gmap[key]
        query = 'INSERT INTO stock_price (symbol, last_price) VALUES ("{0}", {1})'.format(key, gmap[key])
        try:
        #    print query
            cur = conn.cursor()  
            cur.execute(query) 
        except:
            print "error!"
            continue
    cur.close()
    conn.commit()

            
if __name__ == '__main__':
    
    threadlist = []     
    name_list = get_name('company_list.txt')        
    for u in name_list:
        t = Thread(target=th, args=(u,))
        t.start()
        threadlist.append(t)
    
    for b in threadlist:
        b.join()
        
    login_info = get_login_info()
    conn = login(login_info)
    create_db(conn)
    create_table(conn)
    insert_once(gmap, conn)
    
    conn.close()


    
