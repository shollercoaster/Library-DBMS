import mysql.connector as mycon
import names 
import uuid
import random 
import utils as utils
from datetime import datetime

author_names = []
genres = ["Comedy", "Action", "Fantasy", "Literature", "Science", "Informational", "Cook-Book", "Romance", "Sci-Fi", "Thriller", "Adventure", "Fiction", "Crime"]
types = ["Novella", "Storybook", "Informational", "Magazine"]

for iter in range(0, 20): 
    author_names.append(names.get_full_name())

def create_table_book(): 
    con= mycon.connect(host="localhost",user="root",password="Android@291296", database="school")
    str1="CREATE TABLE book (uuid varchar(255), name varchar (255), author varchar (255), genre varchar (255), type varchar (255), issued_by varchar (255))"
    cur=con.cursor()
    cur.execute(str1)
    print("table created successfully")
    con.close()


# try: 
#     create_table_book()

# except Exception as e:
#     print("Never Mind ")

# finally: 
#     connection = mycon.connect(host="localhost",user="root",password="Android@291296", database="school")
#     cursor = connection.cursor()

#     for iter in range(0, 100):
#         book_name = "book_" + str(iter)
#         id = uuid.uuid4()
#         converted = str(id)
#         uuid_val = converted
#         author_name = random.choice(author_names)
#         genre = random.choice(genres)
#         type = random.choice(types)
#         q = "Insert into book (uuid, name, author, genre, type, issued_by) VALUES (%s, %s, %s, %s, %s, %s)" 
#         values = (uuid_val, book_name, author_name, genre, type, "")
#         cursor.execute(q, values)
#         connection.commit()

#     print("records inserted successfully ")
#     connection.close()

def populate_user(): 
    con= mycon.connect(host="localhost",user="root",password="Android@291296", database="school")
    cursor = con.cursor()

    for iter in range(0, 100): 
        id = uuid.uuid4()
        converted = str(id)
        username = "user_" + str(iter)
        password = "pass_" + str(iter)
        query = "insert into user (uuid, username, password, date_of_birth, email, phone_number, is_admin) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (converted, username, password, "03-11-2003", "saumyachat03@gmail.com", "1234567890", False)
        cursor.execute(query, values)
        con.commit()

    print("Done")
    con.close()

def get_all_user_uuids(cursor): 
    uuids = []
    sql = "select uuid from user"
    cursor.execute(sql)
    user_uuids = cursor.fetchall()
    for uuid in user_uuids: 
        uuids.append(uuid[0])
    
    return uuids

def get_all_book_uuids(cursor):
    uuids = []
    sql = "select uuid from book"
    cursor.execute(sql)
    book_uuids = cursor.fetchall()
    for uuid in book_uuids: 
        uuids.append(uuid[0])

    return uuids


def lend_books_to_random_users(): 
    connection = utils.table_connection()
    cursor = connection.cursor()
    user_uuids =  get_all_user_uuids(cursor)
    book_uuids = get_all_book_uuids(cursor)
    for (user, book) in zip(user_uuids, book_uuids): 
        sql = "update book set issued_by = %s, date_of_issue = %s where uuid = %s"
        cursor.execute(sql, (user, datetime.now(), book,))
        try: 
            connection.commit()
            print("Record Updated")

        except Exception as e:
            print(e)
            print("There was an error.")
    
    connection.close()

# populate_user()
# lend_books_to_random_users()