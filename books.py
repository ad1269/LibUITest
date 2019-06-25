import sys
import pandas as pd
import numpy as np

from os import path
import zipfile

### SETUP CODE ###
book_data = None

def load_books():
    global book_data
    if not np.all(list(map(path.exists, ["BX-Books.csv", "BX-Book-Ratings.csv", "BX-Users.csv"]))):
        data = zipfile.ZipFile("Book-Data.zip")
        data.extractall()

    book_data = pd.read_csv("BX-Books.csv", sep=";", encoding="latin-1", error_bad_lines=False, warn_bad_lines=False,
        skiprows=1, names=['ISBN', 'Title', 'Author', 'Year', 'Publisher', 'IURL-S', 'IURL-M', 'IURL-L'])

### FUNCTIONALITY ###

def search_book(search_string):
    titles = book_data.as_matrix(columns=["Title"]).reshape(-1,)
    results = []

    def prefix_match(search_string, title):
        search_string, title = search_string.lower(), title.lower()
        if len(search_string) > len(title):
            return False

        for c1, c2 in zip(search_string, title):
            if c1 != c2:
                return False
        return True

    def substr_match(search_string, title):
        search_string, title = search_string.lower(), title.lower()
        if len(search_string) > len(title):
            return False

        for c1, c2 in zip(search_string, title):
            if c1 != c2:
                return False
        return True

    for title in titles:
        if prefix_match(search_string, title):
            results.append(title)

    return results


def list_books(num):
    df = book_data.head(num)
    return list(df["Title"])

### COMMAND LINE PARSING ###

def lookup_action(argc, argv):
    actions = {"search": 0, "list": 1}

    if argc <= 1:
        return 1, 10

    if argv[1] not in actions:
        raise ValueError("Unknown action given.")

    return actions[argv[1]]

"""
Command Line Usage:

python3 books.py action

Possible Actions:
python3 books.py search "search string"
python3 books.py list NUMBER
"""
def parse_args(argc, argv):

    # Lookup action
    action_number = lookup_action(argc, argv)

    # Call appropriate function
    if action_number == 0:
        if len(argv) > 3:
            raise ValueError("search takes exactly 1 argument.")

        results = search_book(argv[2])
        print(results)
        print(len(results), "results found.")
    elif action_number == 1:
        if len(argv) > 3:
            raise ValueError("list takes exactly 1 argument.")

        num = 0
        try:
            num = int(argv[2])
        except ValueError:
            raise ValueError("Argument to list must be an integer.")

        print(list_books(num))
    else:
        raise NotImplementedError()

    #print(argc, argv)

if __name__ == '__main__':
    load_books()
    parse_args(len(sys.argv), sys.argv)