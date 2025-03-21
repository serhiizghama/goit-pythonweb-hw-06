from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Student, Grade, Subject, Teacher, Group
from sqlalchemy.sql import select

# 🔗 Налаштування БД
DATABASE_URL = "postgresql://postgres:password@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)


def select_1():
    """Знайти 5 студентів із найбільшим середнім балом з усіх предметів."""
    session = Session()
    result = (
        session.query(Student.name, func.avg(Grade.grade).label("avg_grade"))
        .join(Grade)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .limit(5)
        .all()
    )
    session.close()
    return result


def select_2(subject_id):
    """Знайти студента із найвищим середнім балом з певного предмета."""
    session = Session()
    result = (
        session.query(Student.name, func.avg(Grade.grade).label("avg_grade"))
        .join(Grade)
        .filter(Grade.subject_id == subject_id)
        .group_by(Student.id)
        .order_by(func.avg(Grade.grade).desc())
        .first()
    )
    session.close()
    return result


def select_3(subject_id):
    """Знайти середній бал у групах з певного предмета."""
    session = Session()
    result = (
        session.query(Group.name, func.avg(Grade.grade).label("avg_grade"))
        .join(Student, Student.group_id == Group.id)
        .join(Grade, Grade.student_id == Student.id)
        .filter(Grade.subject_id == subject_id)
        .group_by(Group.id)
        .all()
    )
    session.close()
    return result


def select_4():
    """Знайти середній бал на потоці (по всій таблиці оцінок)."""
    session = Session()
    result = session.query(func.avg(Grade.grade)).scalar()
    session.close()
    return result


def select_5(teacher_id):
    """Знайти які курси читає певний викладач."""
    session = Session()
    result = (
        session.query(Subject.name)
        .filter(Subject.teacher_id == teacher_id)
        .all()
    )
    session.close()
    return result


def select_6(group_id):
    """Знайти список студентів у певній групі."""
    session = Session()
    result = (
        session.query(Student.name)
        .filter(Student.group_id == group_id)
        .all()
    )
    session.close()
    return result


def select_7(group_id, subject_id):
    """Знайти оцінки студентів у окремій групі з певного предмета."""
    session = Session()
    result = (
        session.query(Student.name, Grade.grade)
        .join(Grade)
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
        .all()
    )
    session.close()
    return result


def select_8(teacher_id):
    """Знайти середній бал, який ставить певний викладач зі своїх предметів."""
    session = Session()
    result = (
        session.query(func.avg(Grade.grade))
        .join(Subject, Grade.subject_id == Subject.id)
        .filter(Subject.teacher_id == teacher_id)
        .scalar()
    )
    session.close()
    return result


def select_9(student_id):
    """Знайти список курсів, які відвідує певний студент."""
    session = Session()
    result = (
        session.query(Subject.name)
        .join(Grade)
        .filter(Grade.student_id == student_id)
        .distinct()
        .all()
    )
    session.close()
    return result


def select_10(student_id, teacher_id):
    """Список курсів, які певному студенту читає певний викладач."""
    session = Session()
    result = (
        session.query(Subject.name)
        .join(Grade)
        .filter(Grade.student_id == student_id, Subject.teacher_id == teacher_id)
        .distinct()
        .all()
    )
    session.close()
    return result


def select_11(teacher_id, student_id):
    """Середній бал, який певний викладач ставить певному студентові."""
    session = Session()
    result = (
        session.query(func.avg(Grade.grade))
        .join(Subject)
        .filter(Subject.teacher_id == teacher_id, Grade.student_id == student_id)
        .scalar()
    )
    session.close()
    return result


def select_12(group_id, subject_id):
    """Оцінки студентів у певній групі з певного предмета на останньому занятті."""
    session = Session()
    subquery = (
        session.query(
            Grade.student_id,
            func.max(Grade.date_received).label("last_date")
        )
        .join(Student)
        .filter(Student.group_id == group_id, Grade.subject_id == subject_id)
        .group_by(Grade.student_id)
        .subquery()
    )

    result = (
        session.query(Student.name, Grade.grade)
        .join(Grade)
        .join(subquery, (Grade.student_id == subquery.c.student_id) &
                        (Grade.date_received == subquery.c.last_date))
        .all()
    )
    session.close()
    return result


def run_all_queries():
    """Запускає всі запити один за одним і виводить результати в консоль."""
    queries = [
        ("🔝 Top 5 students", select_1, []),
        ("🏆 Top student by subject", select_2, [1]),
        ("📊 Average by group + subject", select_3, [1]),
        ("🌍 Global average", select_4, []),
        ("📚 Subjects by teacher", select_5, [1]),
        ("👨‍🎓 Students in group", select_6, [1]),
        ("📝 Grades in group + subject", select_7, [1, 1]),
        ("🧑‍🏫 Average by teacher", select_8, [1]),
        ("🎒 Subjects by student", select_9, [1]),
        ("👨‍🏫📘 Subjects by student + teacher", select_10, [1, 1]),
        ("📈 Avg grade from teacher to student", select_11, [1, 1]),
        ("⏱ Last grades in group + subject", select_12, [1, 1]),
    ]

    for i, (description, func_select, args) in enumerate(queries, start=1):
        print("—" * 50)
        print(f"{i}. {description}")
        result = func_select(*args)
        if result:
            if isinstance(result, list):
                for row in result:
                    print("  ➤", row)
            else:
                print("  ➤", result)
        else:
            print("  ⚠️  Немає даних")
    print("—" * 50)


if __name__ == "__main__":
    run_all_queries()
