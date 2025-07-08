import pymssql
import json

with open("gi.conf", "r") as f:
    secrets = json.load(f)
# Parametri di connessione per pymssql
DB_SERVER = secrets["db_server"]
DB_DATABASE = secrets["db_database"]
DB_USERNAME = secrets["db_username"]
DB_PASSWORD = secrets["db_password"]

#----------------DB----------------------------
def get_sqlserver_connection():
   """
    Crea una connessione a SQL Server usando pymssql.
    :param server: nome o indirizzo del server SQL
    :param database: nome del database
    :param username: nome utente SQL
    :param password: password SQL
    :return: oggetto connessione pymssql
    """
   return pymssql.connect(server=DB_SERVER, user=DB_USERNAME, password=DB_PASSWORD, database=DB_DATABASE)

# Funzione per eseguire una query SQL e restituire il primo valore come stringa
def execute_query_return_string(conn, query):
    """
    Esegue una query SQL passata come parametro e ritorna il primo valore della prima riga come stringa.
    :param conn: oggetto connessione pymssql
    :param query: query SQL da eseguire
    :return: valore come stringa oppure None se nessun risultato
    """
    cursor = conn.cursor()
    cursor.execute(query)
    row = cursor.fetchone()
    cursor.close()    
    return row

# Funzione per chiamare una stored procedure con un parametro stringa e restituire una stringa
def call_stored_procedure(conn, proc_name, input_param):
    """    
    :param conn: oggetto connessione pymssql
    :param proc_name: nome della stored procedure
    :param input_param: parametro stringa da passare
    :return: stringa restituita dalla stored procedure
    """
    cursor = conn.cursor()
    cursor.callproc(proc_name, (input_param,))
    row = cursor.fetchone()
    cursor.close()
    return row

def call_stored_procedure_two_params(conn, proc_name, graph_mode, value_mode):
    """
    :param proc_name: nome della stored procedure
    :param graph_mode: parametro intero (ad esempio 1, 2, 3, 4)
    :param value_mode: parametro stringa (varchar)
    :return: prima riga restituita dalla stored procedure
    """
    cursor = conn.cursor()
    cursor.callproc(proc_name, (graph_mode, value_mode))
    rows = cursor.fetchall()
    cursor.close()
    return rows