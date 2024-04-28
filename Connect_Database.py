import pypyodbc as odbc

DRIVER = "SQL Server"
SERVER = "LAPTOP-3NMAAD6T"
DATABASE = "Arabisqly"

def connect_to_database(driver, server, database):
    connection_string = f'''
        DRIVER={{{driver}}};
        SERVER={server};
        DATABASE={database};
        Trust_Connection=yes
    '''
    connection = odbc.connect(connection_string)
    inner_cursor = connection.cursor()
    return inner_cursor, connection
