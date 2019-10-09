import sqlite3 
def fetch(paraname, dbname, tbname):
    """fetching colums data from database
    connect with the myTable database """
    connection = sqlite3.connect(dbname) 
# cursor object 
    crsr = connection.cursor() 
# execute the command to etch all the data from the table emp 
    crsr.execute(f"SELECT {paraname} FROM {tbname}") 
# store all the fetched data in the ans variable 
    ans= crsr.fetchall() 
# loop to print all the data
    x=[]
    for i in ans: 
	    x.append(i)
    return x    
#testing
if __name__ == '__main__':
    print(fetch('time','vgu.db','therm'))
