import mysql.connector as mycon
import utils as utils
from os import system
import time


def handle_admin_cases(choice): 
    if choice == 1: 
        utils.print_all_users()
        utils.display_admin_options()
        handle_admin_cases(int(input()))

    elif choice == 2: 
        utils.print_all_books()
        utils.display_admin_options()
        handle_admin_cases(int(input()))

    elif choice == 3: 
        utils.view_all_authors()
        utils.display_admin_options()
        handle_admin_cases(
        int(input()))

    elif choice == 4: 
        utils.display_lent_books_information()
        utils.display_admin_options()
        handle_admin_cases(int(input()))

    elif choice == 5: 
        utils.make_admin()
        utils.display_admin_options()
        handle_admin_cases(int(input()))
    
    elif choice == 6: 
        utils.display_main_menu()
        render_cases(int(input()))

    else: 
        print("Invalid Input")

def handle_book_lend_cases(choice, member_id): 
    if choice == 1: 
            (book_name, fine) = utils.check_for_pending_books(member_id)
            if fine is not None: 
                print("You have a pending book ")
                print("Book Name-> ",book_name)
                print("Due -> ", fine)
                
            else:  
                book_names = utils.display_book_names() 
                print("These are the list of available books. Enter one of the above names (Case sensitive) ")
                book_name = input()
                if book_name in book_names: 
                    utils.lend_book(book_name, member_id)
                    utils.display_book_lending_options()
                    handle_book_lend_cases(int(input()), member_id)

                else: 
                    print("The book name you entered is not correct. Please try again")
                    time.sleep(3)
                    handle_book_lend_cases(1, member_id)

    elif choice == 2: 
        system('cls')
        print("Enter the name of the book you want to return !!")
        book_name = input()
        if utils.check_book_validations(book_name, member_id):
            utils.return_book(book_name)
            utils.display_book_lending_options()
            handle_book_lend_cases(int(input()), member_id)

        else: 
            print("The book name you entered either doesnt exist or does not need to be entered !")
            time.sleep(2)
            handle_book_lend_cases(2, member_id)

    elif choice == 3: 
            utils.add_book()
            utils.display_book_lending_options()
            handle_book_lend_cases(int(input()), member_id)

    elif choice == 4: 
        exit()
    
    elif choice == 5: 
        utils.display_main_menu()
        render_cases(int(input()))

    else: 
        print("Invalid Input")
        return 

def render_cases(choice):
    if choice == 1: 
        try:
            utils.create_database()
            utils.create_table()

        except Exception as e:
            print(e)
            print("UNABLE TO CREATE TABLE !!")

        finally: 
            utils.input_and_save_user()
            print("Your membership has been created !! ")
            print("Have a nice day !")
            utils.display_main_menu()
            render_cases(int(input()))

    elif choice == 2:
        member_uuid = utils.login_member()
        if member_uuid: 
            (book_name, fine) = utils.check_for_pending_books(member_uuid)
            if fine is not None: 
                print("You have a pending book ")
                print("Book Name-> ",book_name)
                print("Due -> ", fine)
            utils.display_book_lending_options()
            handle_book_lend_cases(int(input()), member_uuid)

        else: 
            print("User not found ! Please try again ")

    elif choice == 3: 
        system('cls')
        print("Enter Username: ")
        admin_username = input()
        print("Enter Password: ")
        admin_password = input()
        if (admin_username == "admin" and admin_password == "admin") or utils.is_user_admin(admin_username, admin_password):
            system('cls')
            utils.display_admin_options()
            handle_admin_cases(int(input()))
        else: 
            print("Invalid Credentials. Try again.")
            utils.display_main_menu()
            render_cases(int(input()))

    elif choice == 4: 
        exit(0)

    else: 
        print("Invalid Input !!")



utils.display_main_menu()
render_cases(int(input()))