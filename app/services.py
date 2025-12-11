from .database import get_connection
import datetime

class LibraryService:
    
    # ===== CRUD Buku =====
    def add_book(self, title, author, year):
        with get_connection() as conn:  # buat koneksi baru per request
            cursor = conn.cursor()
            cursor.execute("INSERT INTO books (title, author, year) VALUES (?, ?, ?)", (title, author, year))
            conn.commit()

    def get_books(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM books")
            return cursor.fetchall()

    # ===== CRUD Anggota =====
    def add_member(self, name, email):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO members (name, email) VALUES (?, ?)", (name, email))
            conn.commit()

    def get_members(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM members")
            return cursor.fetchall()

    # ===== Peminjaman =====
    def borrow_book(self, book_id, member_id):
        with get_connection() as conn:
            cursor = conn.cursor()
            loan_date = datetime.date.today().isoformat()
            cursor.execute("INSERT INTO loans (book_id, member_id, loan_date) VALUES (?, ?, ?)",
                           (book_id, member_id, loan_date))
            cursor.execute("UPDATE books SET borrowed_count = borrowed_count + 1 WHERE id=?", (book_id,))
            conn.commit()

    # ===== Pengembalian =====
    def return_book(self, loan_id):
        with get_connection() as conn:
            cursor = conn.cursor()
            return_date = datetime.date.today().isoformat()
            cursor.execute("SELECT loan_date FROM loans WHERE id=?", (loan_id,))
            loan_date = cursor.fetchone()[0]
            days_late = (datetime.date.today() - datetime.datetime.fromisoformat(loan_date).date()).days - 7
            fine = 0
            if days_late > 0:
                fine = days_late * 2000
            cursor.execute("UPDATE loans SET return_date=?, returned=1, fine=? WHERE id=?",
                           (return_date, fine, loan_id))
            conn.commit()

    # ===== Laporan Buku Paling Sering Dipinjam =====
    def most_borrowed_books(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT title, borrowed_count FROM books ORDER BY borrowed_count DESC LIMIT 5")
            return cursor.fetchall()

    # ===== Daftar Peminjaman =====
    def get_loans(self):
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT loans.id, books.title as book, members.name as member, loans.loan_date, loans.return_date, loans.returned, loans.fine
            FROM loans
            JOIN books ON loans.book_id = books.id
            JOIN members ON loans.member_id = members.id
            """)
            return cursor.fetchall()
