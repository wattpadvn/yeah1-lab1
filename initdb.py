#!/usr/bin/python

import sqlite3

def main():
    conn = sqlite3.connect('DB.db')
    ####Create table Detail
    conn.execute('''
        CREATE TABLE detail(
            id  INTEGER PRIMARY KEY AUTOINCREMENT,
            cate  TEXT NOT NULL,
            title    TEXT,
            url    TEXT    NOT NULL,
            content    TEXT,
            created_date    TEXT,
            crawl_source    TEXT    NOT NULL
        );
    ''')

    print("create table cate & detail successfully")
    conn.close()

main()
