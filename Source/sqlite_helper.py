
# ------------ Common helper functions for queries --------------

def get_all_table_names(conn_cursor):
    conn_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;")
    rows = conn_cursor.fetchall()
    names = list()
    for row in rows:
        names.append(row[0])
    return names