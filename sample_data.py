# from app import create_app, db 
# from app.models import User, StudentProfile, CompanyProfile, Internship, Application, Notification 
# from datetime import datetime, timedelta 
# import random 
 
# app = create_app() 
 
# def create_sample_data(): 
#     with app.app_context(): 
#         print("Creating sample data...") 
 
#         # Create sample companies 
#         companies_data = [ 
#             {'name': 'TechCorp Solutions', 'email': 'hr@techcorp.com', 'reg': 'REG1001', 'industry': 'Technology'}, 
#             {'name': 'FinanceHub Inc', 'email': 'careers@financehub.com', 'reg': 'REG1002', 'industry': 'Finance'}, 
#             {'name': 'HealthTech Innovations', 'email': 'jobs@healthtech.com', 'reg': 'REG1003', 'industry': 'Healthcare'}, 
#             {'name': 'EcoGreen Energy', 'email': 'hr@ecogreen.com', 'reg': 'REG1004', 'industry': 'Energy'}, 
#             {'name': 'Creative Design Studio', 'email': 'talent@creativestudio.com', 'reg': 'REG1005', 'industry': 'Design'} 
#         ] 
 
#         companies = [] 
#         for comp_data in companies_data: 
#             if not User.query.filter_by(email=comp_data['email']).first(): 
#                 user = User( 
#                     email=comp_data['email'], 
#                     role='company', 
#                     is_active=True, 
#                     created_at=datetime.utcnow() - timedelta(days=random.randint(30, 365)) 
#                 ) 
#                 user.set_password('Company@123') 
#                 db.session.add(user) 
#                 db.session.flush() 
 
#                 company = CompanyProfile( 
#                     user_id=user.id, 
#                     company_name=comp_data['name'], 
#                     registration_number=comp_data['reg'], 
#                     industry=comp_data['industry'], 
#                     description=f"{comp_data['name']} is a leading company in the {comp_data['industry']} industry.", 
#                     website=f"https://www.{comp_data['name'].lower().replace(' ', '')}.com", 
#                     phone=f"+1-555-{random.randint(100,999)}-{random.randint(1000,9999)}" 
#                 ) 
#                 db.session.add(company) 
#                 companies.append(company) 
#                 print(f"Created company: {comp_data['name']}") 
 
#         # Create sample students 
#         first_names = ['John', 'Jane', 'Michael', 'Sarah', 'David', 'Emily', 'James', 'Lisa'] 
#         last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis'] 
#         courses = ['Computer Science', 'Business Administration', 'Engineering', 'Marketing', 'Finance'] 
 
#         students = [] 
#         for i in range(10): 
#             first = random.choice(first_names) 
#             last = random.choice(last_names) 
#             full_name = f"{first} {last}" 
#             email = f"{first.lower()}.{last.lower()}@student.edu" 
 
#             if not User.query.filter_by(email=email).first(): 
#                 user = User( 
#                     email=email, 
#                     role='student', 
#                     is_active=True, 
#                     created_at=datetime.utcnow() - timedelta(days=random.randint(30, 365)) 
#                 ) 
#                 user.set_password('Student@123') 
#                 db.session.add(user) 
#                 db.session.flush() 
 
#                 student = StudentProfile( 
#                     user_id=user.id, 
#                     full_name=full_name, 
#                     reg_number=f"STU{random.randint(10000, 99999)}", 
#                     course=random.choice(courses), 
#                     year_of_study=random.randint(1, 4), 
#                     cgpa=round(random.uniform(6.0, 9.5), 2), 
#                     phone=f"+1-555-{random.randint(100,999)}-{random.randint(1000,9999)}" 
#                 ) 
#                 db.session.add(student) 
#                 students.append(student) 
 
#         db.session.commit() 
#         print(f"Created {len(students)} sample students") 
 
#         # Create sample internships 
#         titles = [ 
#             'Software Engineering Intern', 'Marketing Intern', 'Financial Analyst Intern', 
#             'UX/UI Design Intern', 'Data Science Intern', 'Business Development Intern' 
#         ] 
 
#         for company in companies: 
#             for _ in range(random.randint(2, 4)): 
#                 deadline = datetime.utcnow() + timedelta(days=random.randint(15, 60)) 
#                 internship = Internship( 
#                     company_id=company.id, 
#                     title=random.choice(titles), 
#                     description=f"Join {company.company_name} as an intern and gain valuable experience.", 
#                     requirements=" Currently pursuing relevant degree\n Strong communication skills\n Team player", 
#                     location=random.choice(['Remote', 'New York', 'San Francisco', 'Boston']), 
#                     stipend=f"${random.choice([1000, 1500, 2000, 2500])}/month", 
#                     duration=random.choice(['3 months', '6 months', 'Summer internship']), 
#                     positions_available=random.randint(1, 3), 
#                     application_deadline=deadline, 
#                     status='open', 
#                     created_at=datetime.utcnow() - timedelta(days=random.randint(5, 30)) 
#                 ) 
#                 db.session.add(internship) 
 
#         db.session.commit() 
#         print("Sample internships created") 
 
#         print("Sample data creation complete!") 
 
# if __name__ == '__main__': 
