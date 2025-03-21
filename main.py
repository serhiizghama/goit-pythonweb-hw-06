import argparse
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Teacher, Group, Student, Subject

DATABASE_URL = "postgresql://postgres:password@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


def create_teacher(name):
    teacher = Teacher(name=name)
    session.add(teacher)
    session.commit()
    print(f"✅ Created Teacher: {teacher.id} — {teacher.name}")


def list_teachers():
    teachers = session.query(Teacher).all()
    for t in teachers:
        print(f"{t.id}: {t.name}")


def update_teacher(id, name):
    teacher = session.query(Teacher).get(id)
    if teacher:
        teacher.name = name
        session.commit()
        print(f"✏️ Updated Teacher {id} to '{name}'")
    else:
        print("⚠️ Teacher not found")


def remove_teacher(id):
    teacher = session.query(Teacher).get(id)
    if teacher:
        session.delete(teacher)
        session.commit()
        print(f"🗑 Removed Teacher {id}")
    else:
        print("⚠️ Teacher not found")


def create_group(name):
    group = Group(name=name)
    session.add(group)
    session.commit()
    print(f"✅ Created Group: {group.id} — {group.name}")


def list_groups():
    groups = session.query(Group).all()
    for g in groups:
        print(f"{g.id}: {g.name}")


def update_group(id, name):
    group = session.query(Group).get(id)
    if group:
        group.name = name
        session.commit()
        print(f"✏️ Updated Group {id} to '{name}'")
    else:
        print("⚠️ Group not found")


def remove_group(id):
    group = session.query(Group).get(id)
    if group:
        session.delete(group)
        session.commit()
        print(f"🗑 Removed Group {id}")
    else:
        print("⚠️ Group not found")


def main():
    parser = argparse.ArgumentParser(description="📚 University Database CLI")
    parser.add_argument("-a", "--action", choices=[
                        "create", "list", "update", "remove"], required=True, help="CRUD action")
    parser.add_argument(
        "-m", "--model", choices=["Teacher", "Group"], required=True, help="Model to act on")

    parser.add_argument("--id", type=int, help="ID for update or delete")
    parser.add_argument("-n", "--name", help="Name for create/update")

    args = parser.parse_args()

    if args.model == "Teacher":
        if args.action == "create":
            create_teacher(args.name)
        elif args.action == "list":
            list_teachers()
        elif args.action == "update":
            update_teacher(args.id, args.name)
        elif args.action == "remove":
            remove_teacher(args.id)

    elif args.model == "Group":
        if args.action == "create":
            create_group(args.name)
        elif args.action == "list":
            list_groups()
        elif args.action == "update":
            update_group(args.id, args.name)
        elif args.action == "remove":
            remove_group(args.id)


if __name__ == "__main__":
    main()
