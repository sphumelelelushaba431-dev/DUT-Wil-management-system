DUT WIL Management System
Group 15 — Tech Titans

HOW TO RUN:
1. Open a terminal in the wil_system/ folder
2. Create and activate a virtual environment:
   python -m venv venv
   venv\Scripts\activate        (Windows)
   source venv/bin/activate     (Mac/Linux)
3. Install dependencies:
   pip install -r requirements.txt
4. Run the application:
   python run.py
5. Open your browser and go to:
   http://127.0.0.1:5000

TEST ACCOUNTS (already in wil.db):
  Student:     [22112211@gmail.com] / [password:student123]
  Coordinator: [coordinator@gmail.com] / [password:co123456]
  Admin:       [admin@gmail.com] / [password:admin123]

ROLES:
  Student     — register, search placements, apply, upload docs
  Coordinator — review applications, approve/reject, notify students
  Admin       — manage users, post placements, view reports
