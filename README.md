**🎓 SmartSchool – Role-Based School Management System**

A FastAPI + MySQL powered portal for Admins, Teachers, and Students.

🚀 Overview

SmartSchool is a full-stack School Management System built using FastAPI, MySQL, Jinja2 Templates, and Bootstrap.
It features secure authentication, role-based dashboards, user management, and a realistic school workflow.

This project is designed to reflect a real-world backend application architecture, and is ideal for learning OR showcasing backend development skills.

🛠️ Tech Stack
Layer	Technology
Backend	FastAPI (Python)
Database	MySQL + SQLAlchemy ORM
Authentication	JWT (JSON Web Tokens)
UI	Jinja2, HTML, CSS, Bootstrap 5
Password Security	Passlib + Bcrypt hashing
Deployment Ready	Render / Railway / Docker
🔐 Key Features
✅ Authentication & Authorization

Secure login using JWT

Password hashing (bcrypt)

Role-based routing & dashboard access

Cookies for session management

🧑‍🏫 Role-based Dashboards
1. Admin Dashboard

View total students, teachers, and notifications

Add new teachers

Add new students

Dynamic stats (counts, recent activity)

2. Teacher Dashboard

View assigned class

View list of students

Mark attendance (future)

Upload marks (future)

3. Student Dashboard

View personal profile

See attendance summary

Class information

Notifications

🧱 Database Models
User Model

Student / Teacher / Admin

Class, Subject, Personal Details

Class Model

Class name

Assigned teacher

Students mapped to class

Attendance Model

Daily attendance

Present/Absent status

Linked to student + class

Notification Model

System-generated notifications

Shown on admin dashboard

📁 Project Structure
SmartSchool/
│
├── main.py
├── create_admin.py
├── requirements.txt
├── start.sh
│
├── app/
│   ├── database.py
│   ├── models/
│   │   ├── user.py
│   │   ├── class_model.py
│   │   ├── attendance_model.py
│   │   └── notification.py
│   ├── routes/
│   │   └── auth.py
│   ├── utils/
│   │   ├── auth_helper.py
│   │   ├── notification_helper.py
│   │   ├── current_user.py
│   │   └── role_checker.py
│   ├── templates/
│   │   ├── login.html
│   │   ├── register.html
│   │   ├── dashboard_admin.html
│   │   ├── dashboard_teacher.html
│   │   └── dashboard_student.html
│   └── static/
│       └── css/
│           └── style.css

⚙️ Setup Instructions
1️⃣ Clone the repository
git clone https://github.com/tejaravi8/smartschool.git
cd smartschool

2️⃣ Create virtual environment
python -m venv venv
venv\Scripts\activate   (Windows)
source venv/bin/activate (Mac/Linux)

3️⃣ Install dependencies
pip install -r requirements.txt

4️⃣ Update MySQL URL in app/database.py
DATABASE_URL = "mysql+mysqlconnector://username:password@localhost/smartschool"

5️⃣ Start the server
uvicorn main:app --reload


Server runs at:
👉 http://127.0.0.1:8000

🌐 Deployment (Render)

SmartSchool is fully deployment-ready.
Use:

pip install -r requirements.txt
bash start.sh


Supports:

Render

Railway

Docker

PythonAnywhere

📸 Screenshots
🔵 Login Page

<img width="1920" height="1020" alt="Screenshot 2025-11-14 211329" src="https://github.com/user-attachments/assets/f55f6f29-57d6-4bb2-80a3-02ea96fc90e4" />
<img width="1920" height="1020" alt="Screenshot 2025-11-14 211311" src="https://github.com/user-attachments/assets/8d54f41b-3192-4a90-ac05-33ad58474915" />

🟣 Admin Dashboard

<img width="1920" height="1020" alt="Screenshot 2025-11-14 211401" src="https://github.com/user-attachments/assets/3aac608b-3217-425d-b399-b2a39ac97d1e" />

🟠 Teacher Dashboard

<img width="1920" height="1020" alt="Screenshot 2025-11-14 211507" src="https://github.com/user-attachments/assets/a96cbf85-7198-401d-b26b-9c6f5ce5c312" />

🟢 Student Dashboard
<img width="1920" height="1020" alt="Screenshot 2025-11-14 211542" src="https://github.com/user-attachments/assets/d2ba44d0-c57b-4f5f-b5b3-cea3ad4d33ce" />

📌 Future Enhancements (Planned)

Student marks management

Subject & timetable management

Attendance graphs per student

Downloadable report cards

Resources / files upload

Chat/parent communication

API endpoints for mobile app

🤝 Contributing

Pull requests are always welcome.
If you spot an issue, feel free to open one!

👤 Author

Botsa Raviteja
📧 Email: botsaraviteja@gmail.com

🔗 GitHub: https://github.com/tejaravi8

💼 LinkedIn: https://linkedin.com/in/botsaraviteja

⭐ Support

If you like this project, please ⭐ star the repo!
