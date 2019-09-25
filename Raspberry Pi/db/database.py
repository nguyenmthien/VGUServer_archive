#!/usr/bin/env python3
# *_* coding: utf-8 *_*

"""Contain functions to create and manipulate a db
createdb(mode, name): create a database named name
writetherm: write the temperature and humidity into the database."""


import sqlite3
import time

def createdb(mode, name):
    """If mode == "thermo", create table with name for data from sensors"""
    if mode == "thermo":
        connection = sqlite3.connect(name) 
        crsr = connection.cursor()
        crsr.execute("""CREATE TABLE IF NOT EXISTS therm (  
        time INTEGER ,
        sensorname INTEGER,  
        temperature REAL,  
        humidity REAL);""")
        connection.commit()
        connection.close()


def writetherm(db_name, sensor_name, temp, humid):
    """Write the temperature and humidity to db"""
    connection = sqlite3.connect(db_name) 
    crsr = connection.cursor() 
    current_time = int(time.time())
    crsr.execute("INSERT INTO therm VALUES (?, ?, ?, ?)",
        (current_time, sensor_name, temp, humid) )
    connection.commit()
    connection.close()

if __name__ == "__main__": 
    createdb("thermo","my.db")
    writetherm("my.db",1,23.3,12.3)
