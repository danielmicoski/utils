import pyodbc 
import json

def get_connection(server,database,username, password, driver='SQL Server'):
    """
    Get SQL Server connection.

    :param String driver: Driver to allow the connection with the data. 
    :param String server: Server name.
    :param String database: Database name.
    :param String username: Username to connect with SQL.
    :param String username: Password to connect with SQL

    :return: Instance of PYODBC Connector
    :rtype: Object
    """
    try:
        conn = pyodbc.connect('DRIVER={0};\
                            SERVER={1};\
                            DATABASE={2};\
                            UID={3};\
                            PWD={4}'.format(
                                driver, server, database, username, password
                            )
        )
        return conn
    except pyodbc.Error as ex:       
         print('Connection Error: {}\n{}'.format(ex.args[0],ex.args[1]))
         return False

def get_cursor(conn):
    """
    Get Connector cursor, which is typically used to manage the context of a fetch operation.

    :param Object conn: SQL Server connectio
    :return: Instance of PYODBC Connector cursor.
    :rtype: Object
    """
    return conn.cursor()

def insert(connector, table, columns, values):
    """
    Insert <values> onto the table <table> inside database metioned in <conn>.

    :param Object connector: Connection with the database. 
    :param String table: Table name.
    :param String[] columns: Columns used to insert elements.
    :param String[] values: Values to insert.

    :return: Message noticing if the transaction occurred correctly or not. 
    :rtype: String
    """
    # TODO: Handle with exceptions.
    columns_struct, values_struct = '(', '('
    if len(columns) == 1:
        columns_struct += columns[0] + ')'
        values_struct += '?)'
    else:
        for i in range(0, len(columns)):
            columns_struct += columns[i] + ','
            values_struct += '?,'
            if i == len(columns)-1:
                columns_struct += ')'
                values_struct += ')'
    insert_records = '''INSERT INTO {0}{1} VALUES{2}'''.format(table,columns_struct, values_struct)
    get_cursor(connector).executemany(insert_records, values)
    connector.commit()
    return "Transaction done! Values inserted in {}".format(table)

def select(connector, query):
    """
    Select values from <query> using <connector>

    :param Object connector: Connection with the database. 
    :param String query: Query to execute in database.
    
    :return: Values returned by query. 
    :rtype: List
    """
    # TODO: Handle with exceptions. 
    # TODO: Think about functionalities to turn select def more easy-to-use.
    """ TODO:
    cursor = conn.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT name, category FROM animal")
    result_set = cursor.fetchall()
    for row in result_set:
        print "%s, %s" % (row["name"], row["category"])
    """
    return list(get_cursor(connector).execute(query))
    
def update(connector, table, columns, values, condition):
    """
    Update values in table <table> giving columns <columns> equals to values <values> where condition <condition>.

    :param Object connector: Connection with the database. 
    :param String table: Table to update values.
    :param String[] columns: Columns from table to update.
    :param String[] values: Values to assign in columns to update.
    :param String condition: Column to use in condition to update.
    
    :return: Message noticing the update. 
    :rtype: String
    """
    # TODO: Handle with exceptions. 
    columns_struct = ''
    for i in range(0, len(columns)):
        if len(columns) == 1 or i == len(columns):
            columns_struct += columns[i] + '=?'
        else:
            columns_struct += columns[i] + '=?,'
    query = '''UPDATE {} SET {} WHERE {} = ?'''.format(table,columns_struct,condition)
    # records_to_update = [(3000, 3), (2750, 4)]
    cursor = get_cursor(connector)
    cursor.executemany(query,values)
    connector.commit()
    return "{} updated successfully".format(table)

def remove(connector, table, condition, value):
    """
    Remove values in table <table> giving a <condition> and a value <value>.

    :param Object connector: Connection with the database. 
    :param String table: Table to update values.
    :param String condition: Column to use in condition to remove.
    :param String value: Values to assign in condition to remove.
    
    :return: Message noticing the remove. 
    :rtype: String
    """
    # TODO: Handle with exceptions. 
    # TODO: Allow multiple removes.
    query = '''DELETE FROM {} WHERE {} = {}'''.format(table, condition, value)
    get_cursor(connector).execute(query)
    connector.commit()
    return "Records form {} removed successfully".format(table)
