# graph visualization using matplotlib library 
import matplotlib.pyplot as plt 
  
def graph_data(p_id,age): 
  
    # plotting the points     
    plt.plot(p_id, age, color='yellow', linestyle='dashed', linewidth = 3, 
    marker='*', markerfacecolor='blue', markersize=12) 
  
    # naming the x axis 
    plt.xlabel('Persons Id') 
  
    # naming the y axis 
    plt.ylabel('Ages') 
  
    # plt.plot(p_id,age) 
    plt.show() 
  
print ("Enter 5 students names:") 
who = [raw_input() for i in range(5)] 
print ("Enter their ages respectively:") 
age = [int(raw_input()) for i in range(5)] 
print ("Enter their ids respectively:") 
p_id = [int(raw_input()) for i in range(5)] 
  
# calling graph function 
graph_data(p_id,age) 