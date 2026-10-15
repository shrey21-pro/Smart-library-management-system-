"""
Smart Library Management System - Unit 2
Data Structures and Collection Management

Structures used:
  Dictionary -> one complete book record
  List       -> the full catalogue (list of dictionaries)
  Tuple      -> ISBN (prefix, code) and publication details (year, edition, publisher)
  Set        -> unique categories, authors, member IDs
  String     -> titles, names, messages (cleaned with string methods)

Run:  python library_system.py
"""

# ---------------------------------------------------------------- constants
FINE_PER_DAY = 0.50          # tuples/constants hold fixed configuration
LOAN_PERIOD_DAYS = 14
LIBRARY_CONFIG = ("Smart Library", FINE_PER_DAY, LOAN_PERIOD_DAYS)

library = []                 # LIST of DICTIONARIES - the full catalogue
member_ids = set()           # SET - unique membership IDs


# ------------------------------------------------------------ string helpers
def clean_text(text):
    """Strip stray spaces and apply Title Case for consistent display."""
    return text.strip().title()


def validate_isbn(isbn):
    """Return True if the ISBN text has exactly 13 digits (hyphens allowed)."""
    digits_only = isbn.replace("-", "").strip()
    return digits_only.isdigit() and len(digits_only) == 13


def make_isbn_tuple(isbn_text):
    """Convert '978-0-13-468599-1' into an immutable (prefix, code) tuple."""
    digits = isbn_text.replace("-", "").strip()
    return (digits[:3], digits[3:])


# ------------------------------------------------------------ book functions
def find_by_id(book_id):
    """Return the record with this ID, or None."""
    for book in library:
        if book["book_id"] == book_id:
            return book
    return None


def add_book(book_id, title, author, category, isbn, price, publication=None):
    """Add a new book record unless the ID already exists."""
    if find_by_id(book_id) is not None:
        print("Book already exists")
        return False
    if not validate_isbn("".join(isbn)):
        print("Invalid ISBN")
        return False
    library.append({
        "book_id": book_id,
        "title": clean_text(title),
        "author": clean_text(author),
        "category": clean_text(category),
        "isbn": isbn,                      # tuple
        "publication": publication,        # tuple (year, edition, publisher)
        "price": price,
        "available": True,
    })
    print("Book added successfully")
    return True


def find_by_title(title):
    """Case-insensitive title search. Returns the record or None."""
    for book in library:
        if book["title"].lower() == title.strip().lower():
            return book
    return None


def search_keyword(keyword):
    """All books whose title contains the keyword (string find())."""
    return [b for b in library if b["title"].lower().find(keyword.lower()) != -1]


def find_by_author(author_name):
    """List of every book by the given author."""
    return [b for b in library if b["author"].lower() == author_name.strip().lower()]


def update_book(book_id, field, new_value):
    """Overwrite a single field of an existing record."""
    book = find_by_id(book_id)
    if book is None:
        print("Book Not Found")
        return False
    if field not in book:
        print("Unknown field")
        return False
    book.update({field: new_value})        # dictionary update()
    print("Book updated successfully")
    return True


def remove_book(book_id):
    """Permanently withdraw a book."""
    book = find_by_id(book_id)
    if book is None:
        print("Book Not Found")
        return False
    library.remove(book)                   # list remove()
    print("Book removed successfully")
    return True


def borrow_book(book_id):
    book = find_by_id(book_id)
    if book is None:
        print("Book Not Found")
    elif not book["available"]:
        print("Book is already borrowed")
    else:
        book["available"] = False
        print("Book borrowed")


def return_book(book_id):
    book = find_by_id(book_id)
    if book is None:
        print("Book Not Found")
    else:
        book["available"] = True
        print("Book returned")


# ---------------------------------------------------------- report functions
def unique_categories():
    """SET of distinct categories - duplicates discarded automatically."""
    return set(book["category"] for book in library)


def unique_authors():
    return {book["author"] for book in library}


def count_available():
    count = 0
    for book in library:
        if book["available"] is True:
            count += 1
    return count


def available_books():
    return [b for b in library if b["available"]]


def borrowed_books():
    return [b for b in library if not b["available"]]


def sorted_titles():
    titles = [b["title"] for b in library]
    titles.sort()
    return titles


def books_by_genre():
    """Dictionary mapping category -> list of titles."""
    groups = {}
    for book in library:
        groups.setdefault(book["category"], []).append(book["title"])
    return groups


def register_member(member_id):
    """Sets reject duplicate registrations."""
    if member_id in member_ids:
        print("Member already registered")
        return False
    member_ids.add(member_id)
    print("Member registered")
    return True


def library_report():
    """Formatted report built with f-strings and join()."""
    lines = [f"--- {LIBRARY_CONFIG[0]} Report ---",
             f"Total books      : {len(library)}",
             f"Available        : {count_available()}",
             f"Borrowed         : {len(library) - count_available()}",
             f"Categories       : {', '.join(sorted(unique_categories()))}",
             f"Authors          : {', '.join(sorted(unique_authors()))}"]
    return "\n".join(lines)


def display_book(book):
    if book is None:
        print("Book Not Found")
        return
    prefix, code = book["isbn"]            # tuple unpacking
    status = "Available" if book["available"] else "Borrowed"
    print(f"{book['book_id']} | {book['title']} | {book['author']} | "
          f"{book['category']} | ISBN {prefix}-{code} | ${book['price']:.2f} | {status}")


# --------------------------------------------------------------- demo / menu
def load_sample_data():
    add_book("B1042", "  the great gatsby ", "f. scott fitzgerald", "fiction",
             ("978", "0743273565"), 10.99, (1925, "1st Edition", "Scribner"))
    add_book("B1043", "dune", "frank herbert", "sci-fi",
             ("978", "0441172719"), 14.50, (1965, "1st Edition", "Chilton"))
    add_book("B1044", "1984", "george orwell", "fiction",
             ("978", "0451524935"), 9.99, (1949, "1st Edition", "Secker"))
    add_book("B1045", "animal farm", "george orwell", "fiction",
             ("978", "0451526341"), 8.99, (1945, "1st Edition", "Secker"))
    add_book("B1046", "a brief history of time", "stephen hawking", "science",
             ("978", "0553380163"), 16.00, (1988, "1st Edition", "Bantam"))


def main():
    load_sample_data()
    print()
    print(library_report())
    print("\nSorted titles:", sorted_titles())
    print("Unique categories:", sorted(unique_categories()))
    print("By genre:", books_by_genre())
    print("\nSearch 'DUNE':")
    display_book(find_by_title("DUNE"))
    print("Search 'Emma':")
    display_book(find_by_title("Emma"))
    borrow_book("B1043")
    print("Available count:", count_available())


if __name__ == "__main__":
    main()
