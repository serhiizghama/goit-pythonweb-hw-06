import random
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from faker import Faker
from models import Base, Group, Student, Teacher, Subject, Grade

fake = Faker()

DATABASE_URL = "postgresql://postgres:password@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


def clear_data():
    print("🧹 Clearing existing data...")
    session.query(Grade).delete()
    session.query(Student).delete()
    session.query(Subject).delete()
    session.query(Teacher).delete()
    session.query(Group).delete()
    session.commit()
    print("✅ Data cleared.")


def create_groups():
    return [Group(name=f"Group {i+1}") for i in range(3)]


def create_teachers():
    return [Teacher(name=fake.name()) for _ in range(random.randint(3, 5))]


def create_subjects(teachers):
    subject_names = [
        "Math", "Biology", "History", "Literature",
        "Physics", "Chemistry", "Philosophy", "Programming"
    ]
    subjects = []
    for name in random.sample(subject_names, k=random.randint(5, 8)):
        teacher = random.choice(teachers)
        subjects.append(Subject(name=name, teacher=teacher))
    return subjects


def create_students(groups):
    return [
        Student(name=fake.name(), group=random.choice(groups))
        for _ in range(random.randint(30, 50))
    ]


def create_grades(students, subjects):
    grades = []
    for student in students:
        subjects_sample = random.sample(
            subjects, k=random.randint(3, len(subjects)))
        for subject in subjects_sample:
            for _ in range(random.randint(5, 20)):
                grade = Grade(
                    student=student,
                    subject=subject,
                    grade=round(random.uniform(60, 100), 2),
                    date_received=fake.date_between(
                        start_date='-1y', end_date='today')
                )
                grades.append(grade)
    return grades


def seed():
    print("🌱 Seeding database...")

    # Групи
    groups = create_groups()
    session.add_all(groups)

    # Викладачі
    teachers = create_teachers()
    session.add_all(teachers)

    # Предмети
    subjects = create_subjects(teachers)
    session.add_all(subjects)

    # Студенти
    students = create_students(groups)
    session.add_all(students)

    session.commit()

    # Оцінки
    grades = create_grades(students, subjects)
    session.add_all(grades)

    session.commit()
    print("✅ Seeding complete.")


if __name__ == "__main__":
    Base.metadata.create_all(engine)
    clear_data()
    seed()
    session.close()
    print("👋 All done!")
