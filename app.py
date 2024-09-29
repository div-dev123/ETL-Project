import os
import mysql.connector
from sqlalchemy import create_engine
import pandas as pd
import numpy as np

# Get MySQL connection details from environment variables
mysql_host = os.getenv('MYSQL_HOST', 'localhost')
mysql_user = os.getenv('MYSQL_USER', 'root')
mysql_password = os.getenv('MYSQL_PASSWORD', 'd1v2a3s4')
mysql_database = os.getenv('MYSQL_DATABASE', 'etl_db')

# Create a connection to MySQL database using MySQL connector
connection = mysql.connector.connect(
    host=mysql_host,         # Hostname
    user=mysql_user,         # Username
    password=mysql_password, # Password
    database=mysql_database  # Database/schema
)

# Create an engine for SQLAlchemy
engine = create_engine(f'mysql+mysqlconnector://{mysql_user}:{mysql_password}@{mysql_host}/{mysql_database}')

# Check the connection (optional)
if connection.is_connected():
    print("Connected to MySQL database")
else:
    print("Connection failed")

df = pd.read_csv('orders.csv')

df.replace(['Not Available', 'unknown'], np.nan, inplace=True)

df.columns = df.columns.str.lower()

df.columns = df.columns.str.replace(' ','_')

df['discount'] = df['list_price'] * df['discount_percent'] * 0.01

df['sale_price'] = df['list_price'] - df['discount']

df['profit'] = df['sale_price'] - df['cost_price']

df['order_date'] = pd.to_datetime(df['order_date'], format="%Y-%m-%d")

df.drop(columns=['list_price', 'cost_price', 'discount_percent'], inplace=True)

# Load data into MySQL
df.to_sql('df_orders', con=engine, if_exists='replace', index=False)

connection.close()
