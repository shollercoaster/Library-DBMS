import mysql.connector as mycon
from os import system 
import uuid
import re 
from datetime import datetime
from datetime import timedelta 

# FUNCTON SECTION STARTS
def display_book_lending_options(): 
    print("1) Lend a book")
    print("2) Return a book ")
    print("3) Add a book ")
    print("4) Exit")
    print("5) Previous Menu ")

def display_admin_options():
    print("1) View all users")
    print("2) View all books")
    print("3) View all authors")
    print("4) View lent books information")
    print("5) Make someone admin")
    print("6) Previous Menu")

def display_main_menu(): 
    print("WELCOME TO BOOKAHOLICS LIBRARY! \n")
    print("1) New Membership ")
    print("2) Existing Account ")
    print("3) Admin Account")
    print("4) Exit ")
    print("Enter choice")

def display_book_names():
    connection = table_connection()
    cursor = connection.cursor()
    sql = "select name from book"
    cursor.execute(sql)
    results = cursor.fetchall()
    connection.close()

    books = []
    for record in results: 
        books.append(record[0])
        print(record[0])

    return books 

def print_all_books():
    connection = table_connection()
    cursor = connection.cursor()
    sql = "select name from book"
    cursor.execute(sql)
    books = cursor.fetchall()
    for book in books: 
        print(book[0])

    connection.close()

def view_all_authors():
    connection = table_connection()
    cursor = connection.cursor()
    sql = "select distinct author from book"
    cursor.execute(sql)
    authors = cursor.fetchall()
    for author in authors: 
        print(author[0])

    connection.close()

def print_all_users():
    connection = table_connection()
    cursor = connection.cursor()
    sql = "select username from user"
    cursor.execute(sql)
    users = cursor.fetchall()
    for user in users: 
        print(user[0])

    connection.close()

def get_formatted_datetime(datetime): 
    date = str(datetime.day) + "-" + str(datetime.month) + "-" + str(datetime.year)
    time = str(datetime.hour) + ":" + str(datetime.minute) + ":" + str(datetime.second)
    return (f"Date: {date} Time: {time} ")

def display_lent_books_information():
    info = []
    connection = table_connection()
    cursor = connection.cursor()
    sql = "select book.name, user.username, book.date_of_issue from book join user on user.uuid = book.issued_by"
    cursor.execute(sql)
    results = cursor.fetchall()
    for ele in results: 
        info_dict = {}
        info_dict['book_name'] = ele[0]
        info_dict['username'] = ele[1]
        info_dict['date_of_issue'] = get_formatted_datetime(ele[2])
        info.append(info_dict)

    connection.close()
    print("USER NAME \t\t BOOK NAME \t\t DATE OF ISSUE")
    for record in info: 
        print(record['username'], "\t\t", record['book_name'], "\t\t", record['date_of_issue'])


def is_user_valid(username, cursor): 
    sql = "select count(*) from user where username = %s"
    cursor.execute(sql, (username,))
    user_count = cursor.fetchone()
    if user_count[0] == 1:
        return True

    return False
        
def make_admin(): 
    connection = table_connection()
    cursor = connection.cursor()
    system('cls')
    print("Enter the name of the user you wantto make admin")
    username = input()
    if is_user_valid(username, cursor): 
        sql = 'update user set is_admin = %s where username = %s'
        cursor.execute(sql, (True, username,))
        try: 
            connection.commit()

        except Exception as e: 
            print(e)
            print("There was an error while trying to update user.")

        finally: 
            connection.close()

def is_user_admin(username, password):
    connection = table_connection()
    cursor = connection.cursor()
    sql = "select is_admin from user where username = %s and password = %s"
    cursor.execute(sql, (username, password,))
    result = cursor.fetchone()
    
    if result[0] == 1: 
        return True

    return False

def is_member_valid(username, password): 
    connection = table_connection()
    cursor = connection.cursor()
    sql = "select uuid from user where username = %s and password = %s"
    cursor.execute(sql, (username, password,))
    result = cursor.fetchone()
    connection.close()
    return result[0]

def return_book(book_name):
    connection = table_connection()
    cursor = connection.cursor()
    sql = "update book set issued_by = %s, date_of_issue = %s where name = %s"
    cursor.execute(sql, ("", None , book_name))
    try: 
        connection.commit()
        print("Successfully returned the book")

    except Exception as e: 
        print(e)
        print("There was an error while returning the book. Please try again !")
            
    finally: 
        connection.close()


def check_book_validations(book_name, member_id): 
    connection = table_connection()
    cursor = connection.cursor()
    sql = "select count(*) from book where name = %s and issued_by = %s"
    cursor.execute(sql, (book_name, member_id,))
    result = cursor.fetchone()
    connection.close()
    if result[0] == 1: 
        return True

    else: 
        return False

def lend_book(book_name, member_id): 
    now = datetime.now()
    formatted =now.strftime('%Y-%m-%d %H:%M:%S')
    connection = table_connection()
    cursor = connection.cursor()
    sql = 'update book set issued_by = %s, date_of_issue = %s where name = %s'
    cursor.execute(sql, (member_id, formatted, book_name,))
    try:
        connection.commit()
        print("Book has been lended successfully !!")

    except Exception as e: 
        print(e)
        print("There was an error while. Please try again later.")
        return

    finally: 
        connection.close()


def login_member(): 
    print("Enter Username ")
    username = input()
    print("Enter Password")
    password = input()

    return is_member_valid(username, password)


def is_username_unique(username):
    connection = table_connection()
    cursor = connection.cursor()
    sql = "select count(*) from user where username = %s "
    cursor.execute(sql, (username,))
    results = cursor.fetchall()
    connection.close()
    count = results[0][0]
    if count > 0: 
        return False 
    else: 
        return True

def is_email_valid(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if (re.search(regex,email)):
        return True

    return False

def table_connection():
    con = mycon.connect(host="localhost",user="root",password="Android@291296", database="school")
    return con

def database_connection(): 
     connection = mycon.connect(host="localhost",user="root",password="Android@291296")
     return connection

def add_book(): 
    print("Enter name of the book ")
    name = input()
    print("Enter name of Author")
    author = input()
    print("Enter Genre of the book ")
    genre = input()
    print("Enter type of the book ")
    type = input()

    connection = table_connection()
    cursor = connection.cursor()
    sql = "Insert into book (uuid, name, author, genre, type) VALUES (%s, %s, %s, %s, %s)" 
    values = (str(uuid.uuid4()), name, author, genre, type)
    cursor.execute(sql, values)
    try: 
        connection.commit()
        print("Book has been added successfully to the database")

    except Exception as e: 
        print(e)
        print("There was an error while trying to add book.")

    finally: 
        connection.close()


def new_membership(values):
    username = values[0]
    password= values[1]
    date_of_birth = values[2]
    email = values[3]
    phone_number= values[4]

    if is_username_unique(username) and is_email_valid(email): 
        connection = table_connection()
        cursor = connection.cursor()
        query = "INSERT INTO USER (uuid, username, password, date_of_birth, email, phone_number) VALUES (%s, %s, %s, %s, %s, %s)" 
        values= (str(uuid.uuid4), username, password, date_of_birth, email, phone_number)
        cursor.execute(query, values)

        try: 
            connection.commit()
            print("RECORD INSERTED SUCCESSFULLY ")

        except Exception as e: 
            print(e)

        finally: 
            connection.close()

    else: 
        print("There seems to be something wrong with the values you have provided. Please try again .!")

def check_for_pending_fines(date_of_issue): 
    now = datetime.now()
    after_one_month = date_of_issue + timedelta(days=30)

    if after_one_month > now:
        difference = after_one_month - now
        return (difference.days * 10)

    return None

def check_for_pending_books(user_id): 
    connection = table_connection()
    cursor = connection.cursor()
    sql = "select name, date_of_issue from book where issued_by = %s"
    cursor.execute(sql, (user_id,))
    results = cursor.fetchone()
    connection.close()
    if results is None: 
        return (None, None)
    else: 
        (book_name, date_of_issue) = results
        if (book_name and date_of_issue): 
            fine = check_for_pending_fines(date_of_issue)
            return (book_name, fine)

def input_and_save_user(): 
    system('cls')
    print("Enter username")
    username = input()
    print("Enter password")
    password = input()
    print("Enter date of birth !")
    date_of_birth = input()
    print("Enter email_id")
    email = input()
    print("Enter Phone number")
    phone_number = input()
    new_membership([username, password, date_of_birth, email, phone_number])

def create_table():
    con= table_connection()
    str1="CREATE TABLE user (uuid varchar(255), username varchar (255), password varchar (255), date_of_birth varchar (255), email varchar (255), phone_number varchar (255))"
    cur=con.cursor()
    cur.execute(str1)
    print("table created successfully")
    con.close()


def create_database():
    con= database_connection()
    cur=con.cursor()
    stmt="show databases"
    cur.execute(stmt)
    flag=False
    for dbname in cur:
        if("school" in dbname):
            flag=True
            break
    if not flag:
        cur.execute("CREATE DATABASE IF NOT EXISTS school;")
        print("database school created")
    else:
        print("database school already exists")
    con.close()

# FUNCTION SECTION ENDS 


# FUNCTIONS ADDED TO CHANGES DATABASE OR TABLE STRUCTURE. WOULD BE REMOVED
def alter_table_book(): 
    connection = table_connection()
    cursor = connection.cursor()
    query = "alter table book add date_of_issue DATETIME"
    cursor.execute(query)
    connection.commit()
    print("Added a new column")
    connection.close()  

def alter_table_user(): 
    connection = table_connection()
    cursor = connection.cursor()
    q = "alter table user alter is_admin set default %s"
    cursor.execute(q, (False,))
    connection.commit()
    print("New column added ")
    connection.close()

# alter_table_book()
# alter_table_user()