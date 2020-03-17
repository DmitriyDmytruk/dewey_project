import psycopg2


try:
   connection = psycopg2.connect(user="dewey_user",
                                 password="dditeam",
                                 host="127.0.0.1",
                                 port="5432",
                                 database="dewey_db")
   cursor = connection.cursor()

   postgres_insert_query = """ INSERT INTO permissions (id, title) VALUES (%s,%s)"""
   record_to_insert = (1, 'can_search_articles')
   cursor.execute(postgres_insert_query, record_to_insert)

   postgres_insert_query = """ INSERT INTO roles (id, title) VALUES (%s,%s)"""
   record_to_insert = (1, 'API User')
   cursor.execute(postgres_insert_query, record_to_insert)

   postgres_insert_query = """ INSERT INTO role_permissions (permission_id, role_id) VALUES (%s,%s)"""
   record_to_insert = (1, 1)
   cursor.execute(postgres_insert_query, record_to_insert)

   postgres_insert_query = """ INSERT INTO users (id, email, is_active, role_id) VALUES (%s,%s,%s,%s)"""
   record_to_insert = (1, 'test@gmail.com', 'f', 1)
   cursor.execute(postgres_insert_query, record_to_insert)

   connection.commit()
   count = cursor.rowcount
   print ("Record inserted successfully into table")

except (Exception, psycopg2.Error) as error :
    # if(connection):
    print("Failed to insert record into table", error)

finally:
    #closing database connection.
    if connection:
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
