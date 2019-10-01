import sqlite3
def fetchnewest(dbname, tbname):
    connection = sqlite3.connect(dbname)
    row = []
    with connection:
        crsr = connection.cursor()    
        crsr.execute(f'SELECT * FROM {tbname}')
        row = crsr.fetchall()  
    return row[len(row)-1]

#testing
if __name__ == '__main__':
    print(fetchnewest('my.db','therm'))