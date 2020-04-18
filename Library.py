"""
Author: Liza
Student ID: 101200678

Commercial Library Management System: OOP codebase
Data structure used: Dictionary(for implementing cart), Binary Search Tree(for fastest search by title)
Persistent data saving: File

"""

from datetime import datetime
from objects import Book, User, BSTree


# exception handling for invalid user input
def input_number(message):
    while True:
        try:
            user_input = int(input(message))
        except ValueError:
            print("Not an integer! Try again.")
            continue
        else:
            return user_input
            break


# let's user add as many books one by one until user enters 'end'
def add_books(bst: BSTree) -> None:
    print("\n***********    ADD BOOK   ***********")

    book_title = input("\nPlease enter the TITLE of the book ('end' to view main menu): ")
    while True:
        author = input("Please enter the AUTHOR of the book: ")
        category = input("Please enter the CATEGORY of the book(fiction/non-fiction/childrens_book/textbooks): ")
        price = input("Please enter the PRICE of the book(number): $")

        book = Book(book_title, author, category, price)

        quantity = input_number("Please enter the QUANTITY in stock( integer ): ")

        # this method stores books by book title in a binary search tree
        bst.insert(book, quantity)

        # dynamically creates file name as per category for persistent data save
        try:
            with open("{}.txt".format(category), "a") as file_by_category:
                file_by_category.write(book.to_string())
                file_by_category.close()
        except FileNotFoundError:
            print("File not found! Category doesn't exist!")

        book_title = input("\nPlease enter the TITLE of the book ('end' to view main menu): ")

        if book_title == "end":
            break


# update any attribute user wishes and shows updated information
def update_book(bst: BSTree) -> None:
    print("\n***********    UPDATE BOOK   ***********")
    book_title = input("\nPlease enter the TITLE of the book to update: ")

    # check if book exists
    lib_entry = bst.search_by_title(book_title)

    if lib_entry is not None:
        updated_book_title = input("Please enter the UPDATED TITLE: ")
        updated_author = input("Please enter the UPDATED AUTHOR name of the book: ")
        updated_category = input("Please enter the UPDATED CATEGORY of the book("
                                 "fiction/non-fiction/childrens_book/textbooks): ")
        updated_price = input("Please enter the UPDATED PRICE of the book: $")
        updated_quantity = input_number("Please enter the UPDATED QUANTITY in stock: ")

        lib_entry.book.book_title = updated_book_title
        lib_entry.book.author = updated_author
        lib_entry.book.category = updated_category
        lib_entry.book.price = updated_price
        lib_entry.number_in_stock = updated_quantity

        print("\nBook " + book_title + " is updated successfully!\n\nUpdated Book Details:")
        bst.print_library_entry(lib_entry)
    else:
        print("Update failed! " + book_title + " is not found in the library!")


# this method shows books by title, whether it's in-stock or out of stock currently
def search_by_title(bst: BSTree) -> None:
    print("\n***********    SEARCH BOOK BY TITLE  ***********")
    book_title: str = input("\nPlease enter the TITLE of the book to search: ")

    lib_entry = bst.search_by_title(book_title)

    if lib_entry is not None and lib_entry.number_in_stock > 0:
        print("\n" + book_title + " is available. \nDetails:")
        bst.print_library_entry(lib_entry)
    elif lib_entry is not None:
        print(book_title + " is temporarily out of stock.")
    else:
        print(" ** " + book_title + " not found!!")


# reads from file category-wise as per user wishes
def search_by_category() -> None:
    print("\n***********    SEARCH BOOK BY CATEGORY  ***********")
    category: str = input("\nPlease enter the CATEGORY name search: ")

    try:
        with open("{}.txt".format(category), "r") as file_by_category:
            print(file_by_category.read())
            file_by_category.close()
    except FileNotFoundError:
        print("File not found! Category doesn't exist!")


def loan_book_menu(bst: BSTree, user: User) -> None:
    print("\n***********    WELCOME TO OUR COLLECTIONS   ***********")
    bst.in_order_traversal()
    print("**************************************************************************************")
    print("Hi " + user.name + ", You have $" + str(user.money))


# let's the user loan a book against small purchasing price
def loan_book(bst: BSTree, user: User):
    loan_book_menu(bst, user)

    book_title = input("Please enter a book title to LOAN('end' to view main menu): ")

    while book_title != "end":
        lib_entry = bst.search_by_title(book_title)
        if lib_entry is not None:
            if int(lib_entry.book.price) > user.money:
                print("Insufficient funds to loan " + book_title)
            else:
                date_entry = input("Please enter the due date (YYYY, MM, DD): ")
                year, month, day = map(int, date_entry.split(','))
                due_date = datetime(year, month, day)
                due_date_str = due_date.strftime("%d-%b-%Y (%H:%M:%S.%f)")

                user.take_loan(lib_entry.book, due_date_str)
                user.withdraw(int(lib_entry.book.price))
                lib_entry.number_in_stock -= 1
        else:
            print(" ** " + book_title + " not found!! **")
        loan_book_menu(bst, user)
        book_title = input("Please enter a book title to LOAN('end' to view main menu): ")


def main_menu() -> None:
    print("\n***********    MAIN MENU   ***********")
    print("1.   ADD books to the library")
    print("2.   SEARCH books by TITLE")
    print("3.   SEARCH books by CATEGORY")
    print("4.   UPDATE book")
    print("5.   LOAN books")
    print("6.   VIEW collection")
    print("7.   VIEW receipt")
    print("8.   VIEW user information")
    print("9.   EXIT")


def main():
    user_name = input("Please enter the user NAME: ")

    user = User(user_name, 50)
    print("\n<-- Welcome to the Library, " + user_name + " -->")
    bst = BSTree()

    while True:
        main_menu()
        user_choice = input("\nPlease select an operation from the menu( 1 - 9 ): ")

        if user_choice == "1":
            add_books(bst)
        if user_choice == "2":
            search_by_title(bst)
        if user_choice == "3":
            search_by_category()
        if user_choice == "4":
            update_book(bst)
        if user_choice == "5":
            loan_book(bst, user)
        if user_choice == "6":
            bst.in_order_traversal()
        if user_choice == "7":
            user.print_receipt()
        if user_choice == "8":
            user.print_user()
        if user_choice == "9":
            print("\nExiting Library...")
            break


if __name__ == "__main__":
    main()
