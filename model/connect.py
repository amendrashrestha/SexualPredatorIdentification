__author__ = 'amendrashrestha'

from pymysql import connect, err, sys, cursors

def conn_db():
    db = connect(host='localhost', port=8889, user='root', password='root86', db='SexualPredator', autocommit=True)
    cur = db.cursor(cursors.DictCursor)
    return cur