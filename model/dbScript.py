__author__ = 'amendrashrestha'

import model.connect as conn

import utilities.IOReadWrite as IO


def loadPredatorFile(filepath):
    predators = IO.read_text_file(filepath)

    for predator in predators:
        connect = conn.conn_db()
        sql = "insert into tbl_train_predator(author) VALUES('%s')" % (predator.strip())
        connect.execute(sql)


def get_users_text(user_id, table_name):
    try:
        connect = conn.conn_db()

        sql = "SELECT text FROM " + table_name + " WHERE author ='%s'"
        connect.execute(sql % user_id)
        user_text = connect.fetchall()

        return ' '.join(single_text['text'] for single_text in user_text)

    finally:
        connect.close()


def get_users_time(user_id, table_name):
    try:
        connect = conn.conn_db()

        sql = "SELECT subString(time, 1,2) as time FROM " + table_name + " WHERE author ='%s'"
        connect.execute(sql % user_id)

        return [time['time'] for time in connect.fetchall()]

    finally:
        connect.close()


def get_users(table_name):
    try:
        connect = conn.conn_db()
        sql = "SELECT author FROM " + table_name + " limit 1"
        connect.execute(sql)

        return [user['author'] for user in connect.fetchall()]

    finally:
        connect.close()