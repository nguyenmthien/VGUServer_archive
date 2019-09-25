# code for update operation 
import sqlite3 
  
# database name to be passed as parameter 
conn = sqlite3.connect('mydatabase.db') 
  
# update the student record 
conn.execute("UPDATE Student SET name = 'Sam' where unix='B113059'") 
conn.commit() 
  
print "Total number of rows updated :", conn.total_changes 
  
cursor = conn.execute("SELECT * FROM Student") 
for row in cursor: 
   print row, 
  
conn.close()