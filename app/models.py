# models.py
class Book:
    def __init__(self, id, title, author, year, borrowed_count=0):
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.borrowed_count = borrowed_count

class Member:
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email

class Loan:
    def __init__(self, id, book_id, member_id, loan_date, return_date, returned=0, fine=0):
        self.id = id
        self.book_id = book_id
        self.member_id = member_id
        self.loan_date = loan_date
        self.return_date = return_date
        self.returned = returned
        self.fine = fine
