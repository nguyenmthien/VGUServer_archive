import sqlite3
import time
def fetchnewest(dbname, tbname):
    """Get latest row of table tbname in file dbname"""
    with sqlite3.connect(dbname) as connection:
        crsr = connection.cursor()    
        crsr.execute(f'SELECT * FROM {tbname} ORDER BY time desc')
        row = crsr.fetchone()
    return row


if __name__ == '__main__':
    t = time.time()
    output = fetchnewest('vgu.db','therm')
    print(output[2])
    print(f"Time ellapsed: {time.time()-t} s")