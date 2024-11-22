import configparser

# Cria o objeto ConfigParser
config = configparser.ConfigParser()

# Lê o arquivo de propriedades (config.ini)
config.read('config.ini')

# Obtém os valores das propriedades
database = config['DEFAULT'].get('database')
dbuser = config['DEFAULT'].get('dbuser')
dbpassword = config['DEFAULT'].get('dbpassword')

# Imprime os valores
print(f"Database: {database}")
print(f"DB User: {dbuser}")
print(f"DB Password: {dbpassword}")


