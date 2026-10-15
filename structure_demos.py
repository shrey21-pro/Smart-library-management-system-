"""Demonstrations of every method listed in Unit 2, Sections 6-10."""


def string_demo():
    print("=== STRINGS ===")
    title = "  the great gatsby  "
    print("original   :", repr(title))
    print("strip()    :", repr(title.strip()))
    clean = title.strip()
    print("upper()    :", clean.upper())
    print("lower()    :", clean.upper().lower())
    print("title()    :", clean.title())
    print("capitalize():", clean.capitalize())
    print("split()    :", "a,b,c".split(","))
    print("join()     :", ", ".join(["Fiction", "Sci-Fi"]))
    print("replace()  :", "Dune".replace("u", "o"))
    print("find()     :", "library".find("brar"), "| missing ->", "library".find("zzz"))
    print("count()    :", "banana".count("a"))
    print("startswith():", "1984".startswith("19"))
    print("endswith() :", "Emma.pdf".endswith(".pdf"))
    print("indexing   :", clean.title()[0], "| slicing:", clean.title()[4:9])
    print("f-string   :", f"{clean.title()} by {'F. Scott Fitzgerald'}")
    print("escapes    : Title\\tAuthor ->", "Title\tAuthor")
    isbn = "978-0-13-468599-1"
    digits = isbn.replace("-", "")
    print("ISBN valid :", digits.isdigit() and len(digits) == 13)
    # Immutability: a method returns a NEW string, original unchanged
    s = "dune"
    s.upper()
    print("immutable  : s is still", s)


def list_demo():
    print("\n=== LISTS ===")
    books = ["1984", "Dune", "Emma"]
    books.append("Atomic Habits");       print("append  :", books)
    books.insert(0, "Zen");              print("insert  :", books)
    books.extend(["Emma", "Ulysses"]);   print("extend  :", books)
    books.remove("Zen");                 print("remove  :", books)
    popped = books.pop(0);               print("pop(0)  :", popped, books)
    print("index   :", books.index("Emma"))
    print("count   :", books.count("Emma"))
    books.sort();                        print("sort    :", books)
    books.reverse();                     print("reverse :", books)
    print("negative index [-1]:", books[-1])
    print("comprehension (len>4):", [t for t in books if len(t) > 4])
    pairs = [["1984", "Orwell"], ["Dune", "Herbert"]]   # nested list
    for title, author in pairs:
        print("nested  :", title, "-", author)
    books.clear();                       print("clear   :", books)


def tuple_demo():
    print("\n=== TUPLES ===")
    isbn = ("978", "0134685991")
    prefix, code = isbn                                 # unpacking
    print("unpacked:", prefix, code)
    publication = (2020, "3rd Edition", "Pearson")      # packing
    year, edition, publisher = publication
    print("publication:", year, edition, publisher)
    nested = ((2020, "3rd"), "Pearson")
    print("nested  :", nested[0][1])
    print("count   :", ("a", "b", "a").count("a"), "| index:", ("a", "b").index("b"))
    try:
        isbn[0] = "979"
    except TypeError as err:
        print("immutable -> TypeError:", err)
    FINE_PER_DAY, LOAN_DAYS = (0.50, 14)               # constants
    print("config  :", FINE_PER_DAY, LOAN_DAYS)


def set_demo():
    print("\n=== SETS ===")
    categories = ["Fiction", "Sci-Fi", "Fiction", "History"]
    unique = set(categories)
    print("de-duplicated:", sorted(unique))
    unique.add("Science");        print("add     :", sorted(unique))
    unique.remove("History");     print("remove  :", sorted(unique))
    unique.discard("Nothing");    print("discard (absent, no error):", sorted(unique))
    fiction = {"Aisha", "Ben", "Chen"}
    scifi = {"Ben", "Divya"}
    print("union        :", sorted(fiction | scifi))
    print("intersection :", sorted(fiction & scifi))
    print("difference   :", sorted(fiction - scifi))
    print("membership   :", "Ben" in fiction)
    members = set()
    for m in ["M1", "M2", "M1"]:
        if m in members:
            print("duplicate registration rejected:", m)
        else:
            members.add(m)
    print("members      :", sorted(members))


def dict_demo():
    print("\n=== DICTIONARIES ===")
    book = {"book_id": "B1042", "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald", "category": "Fiction",
            "available": True, "price": 12.99, "shelf_number": "A-14"}
    print("keys()   :", list(book.keys()))
    print("values() :", list(book.values())[:3], "...")
    print("items()  :", list(book.items())[:2], "...")
    print("get()    :", book.get("price", 0), "| missing ->", book.get("isbn", "n/a"))
    book.update({"available": False, "price": 10.99})
    print("update() :", book["available"], book["price"])
    print("pop()    :", book.pop("shelf_number"))
    print("popitem():", book.popitem())
    catalogue = {"B1042": book,
                 "B1043": {"title": "Dune", "author": "Frank Herbert", "available": True}}
    for book_id, details in catalogue.items():
        print("catalogue:", book_id, "->", details["title"])
    book.clear()
    print("clear()  :", book)


if __name__ == "__main__":
    string_demo()
    list_demo()
    tuple_demo()
    set_demo()
    dict_demo()
