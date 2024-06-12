import pyodbc
import pandas as pd
import os
from datetime import datetime


connection=pyodbc.connect(driver = 'ODBC Driver 17 for SQL Server',
                          server = 'Dhanush\\SQLEXPRESS',
                          database = 'TestDB',
                          trusted_connection = 'yes')

