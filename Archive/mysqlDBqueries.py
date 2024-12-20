# import mysql.connector
# from mysql.connector import Error
# from datetime import datetime

# class mysqlDBqueries:
#     def __init__(self):
#         self.connection = mysql.connector.connect(
#                 host="localhost",   
#                 database="telegram_mine",
#                 user="telegram",        
#                 password="IKnowIts@Visible4u" 
#             )
        
#     def insert_process_data(self, process, status):
#         try:
#             if self.connection.is_connected():
#                 print("Connected to MySQL")

#                 # Insert query
#                 insert_query = """
#                 INSERT INTO track_mining (process, status, datetime)
#                 VALUES (%s, %s, %s);
#                 """

#                 # Data to insert
#                 current_time = datetime.now()
#                 values = (process, status, current_time)

#                 # Execute query
#                 cursor = self.connection.cursor()
#                 cursor.execute(insert_query, values)
#                 self.connection.commit()

#                 print(f"Data inserted: {values}")

#         except Error as e:
#             print(f"Error: {e}")
#         finally:
#             if self.connection.is_connected():
#                 cursor.close()
#                 self.connection.close()
#                 print("MySQL connection closed.")


#     def fetch_last_record(self, process_name):
#         try:
#             cursor = self.connection.cursor(dictionary=True)

#             # Query to fetch the last record
#             query = """
#             SELECT * 
#             FROM track_mining
#             WHERE process = %s
#             ORDER BY datetime DESC
#             LIMIT 1;
#             """
#             cursor.execute(query, (process_name,))
#             record = cursor.fetchone()
#             print(f'record Fetched: {record}')
#             return record

#         except mysql.connector.Error as err:
#             print(f"Error: {err}")
#             return None

#         finally:
#             if self.connection.is_connected():
#                 cursor.close()
#                 self.connection.close()

# # process with their code:
# # 1) wcoin
# # 2) mmm
# # 3) blum
