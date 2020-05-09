def select_cursor(cursor,query,fetch):
    cursor.execute(query)
    return cursor.fetchmany(fetch)
def select(connection,query,fetch = 5):
    return select_cursor(connection.cursor(),query,fetch)
def insert_cursor(cursor,query):
    cursor.execute(query)
def insert(connection,query):
    insert_cursor(connection.cursor(),query)
