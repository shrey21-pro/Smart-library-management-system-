"""Test cases for library_system.py (run: python test_library.py)."""
import io
import contextlib
import library_system as ls

results = []


def reset():
    ls.library.clear()
    ls.member_ids.clear()


def quiet(fn, *a):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        out = fn(*a)
    return out, buf.getvalue().strip()


def check(name, category, condition):
    results.append((name, category, "PASS" if condition else "FAIL"))


def add(book_id="B1", title="Dune", author="Frank Herbert", cat="Sci-Fi",
        isbn=("978", "0441172719")):
    return quiet(ls.add_book, book_id, title, author, cat, isbn, 14.5)


# T1 normal add
reset(); ok, msg = add()
check("T1 Add a new book", "Normal", ok and msg == "Book added successfully" and len(ls.library) == 1)
# T2 duplicate ID
ok, msg = add()
check("T2 Add book with existing ID is rejected", "Duplicate", (not ok) and msg == "Book already exists" and len(ls.library) == 1)
# T3 invalid ISBN
reset(); ok, msg = add(isbn=("978", "123"))
check("T3 ISBN with wrong length is rejected", "Invalid", (not ok) and msg == "Invalid ISBN")
# T4 search normal
reset(); add()
rec, _ = quiet(ls.find_by_title, "Dune")
check("T4 Search existing title", "Normal", rec is not None and rec["author"] == "Frank Herbert")
# T5 search case-insensitive
rec, _ = quiet(ls.find_by_title, "DUNE")
check("T5 Search 'DUNE' matches 'Dune'", "Case sensitivity", rec is not None)
# T6 search empty catalogue
reset(); rec, _ = quiet(ls.find_by_title, "Dune")
check("T6 Search in empty catalogue returns None, no crash", "Boundary", rec is None)
# T7 search missing title
add(); rec, _ = quiet(ls.find_by_title, "Emma")
check("T7 Search for non-existent title", "Invalid", rec is None)
# T8 title cleaning
reset(); add(title="  the great gatsby ")
check("T8 Title stripped and title-cased", "Normal", ls.library[0]["title"] == "The Great Gatsby")
# T9 update normal
reset(); add()
ok, msg = quiet(ls.update_book, "B1", "price", 20.0)
check("T9 Update existing field", "Normal", ok and ls.library[0]["price"] == 20.0)
# T10 update missing ID
ok, msg = quiet(ls.update_book, "ZZ", "price", 1)
check("T10 Update missing book ID", "Invalid", (not ok) and msg == "Book Not Found")
# T11 update unknown field
ok, msg = quiet(ls.update_book, "B1", "colour", "red")
check("T11 Update unknown field", "Invalid", (not ok) and msg == "Unknown field")
# T12 remove
ok, _ = quiet(ls.remove_book, "B1")
check("T12 Remove existing book", "Normal", ok and ls.library == [])
# T13 remove from empty
ok, msg = quiet(ls.remove_book, "B1")
check("T13 Remove from empty catalogue", "Boundary", (not ok) and msg == "Book Not Found")
# T14 unique categories
reset()
add("B1", cat="Fiction"); add("B2", title="Emma", cat="Fiction"); add("B3", title="Cosmos", cat="Science")
check("T14 Duplicate categories removed by set", "Normal", ls.unique_categories() == {"Fiction", "Science"})
# T15 unique categories empty
reset()
check("T15 Unique categories of empty catalogue", "Boundary", ls.unique_categories() == set())
# T16 count available
reset(); add("B1"); add("B2", title="Emma"); quiet(ls.borrow_book, "B1")
check("T16 Count available after one borrow", "Normal", ls.count_available() == 1)
# T17 borrow already borrowed
_, msg = quiet(ls.borrow_book, "B1")
check("T17 Borrow an already borrowed book", "Invalid", msg == "Book is already borrowed")
# T18 return
quiet(ls.return_book, "B1")
check("T18 Return a book restores availability", "Normal", ls.count_available() == 2)
# T19 find by author
reset(); add("B1", author="George Orwell"); add("B2", title="Animal Farm", author="George Orwell"); add("B3", title="Dune")
res, _ = quiet(ls.find_by_author, "george orwell")
check("T19 Find by author returns both books", "Normal", len(res) == 2)
res, _ = quiet(ls.find_by_author, "Nobody")
check("T20 Find by author - none found", "Invalid", res == [])
# T21 sorted titles
reset(); add("B1", title="Dune"); add("B2", title="Emma"); add("B3", title="1984")
check("T21 Titles sorted alphabetically", "Normal", ls.sorted_titles() == ["1984", "Dune", "Emma"])
# T22 keyword search
res, _ = quiet(ls.search_keyword, "mm")
check("T22 Keyword search finds 'Emma'", "Normal", [b["title"] for b in res] == ["Emma"])
# T23 members
reset()
a, _ = quiet(ls.register_member, "M1"); b, msg = quiet(ls.register_member, "M1")
check("T23 Duplicate member ID rejected by set", "Duplicate", a and (not b) and msg == "Member already registered")
# T24 genre grouping
reset(); add("B1", cat="Fiction"); add("B2", title="Emma", cat="Fiction")
check("T24 Books grouped by genre (dict of lists)", "Normal", ls.books_by_genre() == {"Fiction": ["Dune", "Emma"]})
# T25 ISBN validator
check("T25 validate_isbn accepts hyphenated 13-digit", "Normal", ls.validate_isbn("978-0-13-468599-1"))
check("T26 validate_isbn rejects letters", "Invalid", not ls.validate_isbn("978-ABC-468599-1"))
# T27 tuple immutability
reset(); add()
try:
    ls.library[0]["isbn"][0] = "979"
    immutable = False
except TypeError:
    immutable = True
check("T27 ISBN tuple cannot be modified", "Normal", immutable)

width = max(len(r[0]) for r in results)
for name, cat, status in results:
    print(f"{name.ljust(width)}  [{cat}]  {status}")
passed = sum(1 for r in results if r[2] == "PASS")
print(f"\n{passed}/{len(results)} tests passed")
