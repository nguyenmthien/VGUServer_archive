import sqlite3

def createdb(mode, name):
    if mode == "thermo":
        connection = sqlite3.connect("myTable.db") 
        crsr = connection.cursor() 
