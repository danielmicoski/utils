import json
from conn_db \
    import get_connection, get_cursor, insert, select, update, remove

def get_config_file(path):
    with open(path) as json_file:
        return json.load(json_file)

config_json = get_config_file('config.json')

conn = get_connection(
        driver = config_json["database"]["driver"],
        server = config_json["database"]["server"],
        database = config_json["database"]["db_name"],
        username = config_json["database"]["username"],
        password = config_json["database"]["password"]
    )


# Selecting elements
teste_select = select(connector = conn, \
                    query = '''SELECT * from {}'''.format(config_json["database"]["table_teste_name"]))
print(teste_select)
'''
# Inserting elements
teste_insert = insert(connector = conn, \
                    table = config_json["database"]["table_teste_name"], \
                    columns = ['t'], \
                    values = [[1],[1000],[876]])
print(teste_insert)

# Updating elements
teste_update = update(connector = conn, \
                    table = config_json["database"]["table_teste_name"], \
                    columns = ['t'], \
                    condition = 't', \
                    values = [(10,1000),(2,1),(888,876)])
print(teste_update)  

# Removing elements
teste_remove = remove(connector = conn, \
                    table = config_json["database"]["table_teste_name"], \
                    condition = 't', \
                    value = 140)
print(teste_remove)
'''