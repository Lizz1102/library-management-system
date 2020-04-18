"""
Author: Liza
Student ID: 101200678
"""

from builtins import int


class Book:
    def __init__(self, book_title, author, category, price):
        self.book_title = book_title
        self.author = author
        self.category = category
        self.price = price

    # returns a string equivalent of the book object
    def to_string(self) -> str:
        s = "\nTitle: " + self.book_title + "   Author: " + self.author + "   Category: " + self.category \
            + "   Price: " + self.price
        return s


class LibraryEntry:
    def __init__(self, book, number_in_stock):
        self.book = book
        self.number_in_stock = number_in_stock
        self.left = self.right = None


class BSTree:
    def __init__(self):
        self.root = None

    def insert(self, book: Book, quantity: int) -> None:
        key = self.get_int_value(book.book_title)

        new_entry = LibraryEntry(book, quantity)
        if self.root is None:
            self.root = new_entry
            return

        current = parent = self.root
        while current is not None:
            parent = current

            if self.get_int_value(current.book.book_title) == key:  # item exists already
                print(book.book_title + " already exists!\nEnter 'end' to go to main menu to UPDATE " + book.book_title)
                return

            if self.get_int_value(current.book.book_title) > key:
                current = current.left
            else:
                current = current.right

        if self.get_int_value(parent.book.book_title) > key:
            parent.left = new_entry
        else:
            parent.right = new_entry

    def search_by_title(self, book_title: str) -> object:
        key = self.get_int_value(book_title)
        if self.root is None:
            return None

        curr = self.root
        while curr is not None and self.get_int_value(curr.book.book_title) != key:
            if self.get_int_value(curr.book.book_title) > key:
                curr = curr.left
            else:
                curr = curr.right

        if curr is None:
            return None
        return curr

    def in_order_traversal(self) -> None:
        print("\n*************   LIBRARY COLLECTIONS   *************")
        self.recursive_in_order(self.root)
        print("")

    # recursive method to traverse the bst
    def recursive_in_order(self, lib_entry: object) -> None:
        if lib_entry is not None:
            self.recursive_in_order(lib_entry.left)
            if lib_entry.number_in_stock > 0:
                self.print_library_entry(lib_entry)

            self.recursive_in_order(lib_entry.right)

    # Get integer value from string book_title so that it can be used as a key in the bst
    @staticmethod
    def get_int_value(book_title: str) -> int:
        value = 0
        for i in range(0, len(book_title)):
            value += ord(book_title[i])
        return value

    # utility function to display an item from the inventory
    @staticmethod
    def print_library_entry(lib_entry) -> None:
        print("\nTitle: " + lib_entry.book.book_title + "   Author: " + lib_entry.book.author +
              "   Category: " + lib_entry.book.category + "   Price: " + lib_entry.book.price +
              "   Quantity in stock: " + str(lib_entry.number_in_stock))


class User:
    def __init__(self, name, money):
        self.name = name
        self.money = money
        self.bill = 0
        self.num_items = 0
        self.dict_cart = {} # used to store (book, due date) pairs 

    def take_loan(self, book: Book, due_date: str) -> None:
        self.dict_cart[book.book_title] = due_date
        self.bill += int(book.price)
        self.num_items += 1
        print(book.book_title + " is added to cart...")

        print("Books added to cart so far: " + str(self.num_items))

    def withdraw(self, amt) -> None:
        self.money = self.money - amt

    # display user profile
    def print_user(self) -> None:
        print("**********   USER PROFILE   **********")
        print("\n Name: " + self.name + "\n Account Balance: $" + str(self.money))

    # generate receipt
    def print_receipt(self) -> None:
        print("**********   RECEIPT   **********")
        print(" User name: " + self.name + "\n Total bill: $" + str(self.bill) + "\n Total books checked out: " +
              str(self.num_items))
        print(" \nBook\t\t\t\t\tDue Date")
        for x in self.dict_cart.keys():
            print(x + "\t\t\t" + str(self.dict_cart[x]))
