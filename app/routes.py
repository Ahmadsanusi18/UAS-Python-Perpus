# routes.py
from flask import Blueprint, render_template, request, redirect, url_for
from .services import LibraryService

main = Blueprint('main', __name__)
service = LibraryService()

# ===== Halaman Utama =====
@main.route('/')
def index():
    return render_template('index.html')

# ===== Buku =====
@main.route('/books')
def books():
    books = service.get_books()
    return render_template('books.html', books=books)

@main.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        year = int(request.form['year'])
        service.add_book(title, author, year)
        return redirect(url_for('main.books'))
    return render_template('add_book.html')

# ===== Anggota =====
@main.route('/members')
def members():
    members = service.get_members()
    return render_template('members.html', members=members)

@main.route('/add_member', methods=['GET', 'POST'])
def add_member():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        service.add_member(name, email)
        return redirect(url_for('main.members'))
    return render_template('add_member.html')

# ===== Peminjaman & Pengembalian =====
@main.route('/loans', methods=['GET', 'POST'])
def loans():
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'borrow':
            service.borrow_book(int(request.form['book_id']), int(request.form['member_id']))
        elif action == 'return':
            service.return_book(int(request.form['loan_id']))
        return redirect(url_for('main.loans'))
    books = service.get_books()
    members = service.get_members()
    loans = service.get_loans()
    return render_template('loans.html', books=books, members=members, loans=loans)

# ===== Laporan =====
@main.route('/report')
def report():
    top_books = service.most_borrowed_books()
    return render_template('report.html', top_books=top_books)
