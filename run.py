# run.py
from app import create_app
from app.database import initialize_db

initialize_db()
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
