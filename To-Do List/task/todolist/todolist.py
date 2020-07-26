# Write your code here
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread=False')

Base = declarative_base()


class Table(Base):
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    string_field = Column(String)
    date_field = Column(Date)

    def __repr__(self):
        return self.string_field


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def check_day(day):
    if day == 0:
        return "Monday"
    elif day == 1:
        return "Tuesday"
    elif day == 2:
        return "Wednesday"
    elif day == 3:
        return "Thursday"
    elif day == 4:
        return "Friday"
    elif day == 5:
        return "Saturday"
    elif day == 6:
        return "Sunday"


def all_tasks():
    rows = session.query(Table).all()
    row_date = session.query(Table.date_field).all()

    deadline_list = list()

    count = 0
    numerate = 1
    for i in rows:
        date_string = strip_time(row_date[count], 1)
        deadline_list.append(date_string)

        print(str(numerate) + ". " + str(rows[count]) + ". " + str(deadline_list[count]))
        count += 1
        numerate += 1
    pass


def strip_time(date_strip, choice):
    str_date = str(date_strip).strip('()')
    str_date = str_date.strip(',')
    str_date = str_date.strip("datetime.date")
    str_date = str_date.strip("(,)")
    deadlines = datetime.strptime(str_date, '%Y, %m, %d').date()
    if choice == 0:
        return deadlines
    elif choice == 1:
        return str(deadlines.day) + " " + str(deadlines.strftime('%b'))


def missed_tasks():
    tasks_miss = session.query(Table).filter(Table.date_field < datetime.today()).all()
    tasks_date = session.query(Table.date_field).filter(Table.date_field < datetime.today()).all()
    date_list = list()
    num = 1
    counter = 0
    print("Missed tasks:")
    if len(tasks_miss) == 0:
        print("Nothing is missed!")
    else:
        for j in tasks_miss:
            new_date = strip_time(tasks_date[counter], 1)
            date_list.append(new_date)
            print(str(num) + ". " + str(tasks_miss[counter]) + ". " + str(date_list[counter]))
            num += 1
            counter += 1
    print()
    pass


def delete_tasks():
    print("Chose the number of the tasks you want to delete:")
    rows = session.query(Table).all()
    row_date = session.query(Table.date_field).all()

    deadline_list = list()
    date_add = list()

    count = 0
    numerate = 1
    for i in rows:
        date_string = strip_time(row_date[count], 1)
        add_to = strip_time(row_date[count], 0)
        date_add.append(add_to)
        deadline_list.append(date_string)

        print(str(numerate) + ". " + str(rows[count]) + ". " + str(deadline_list[count]))
        count += 1
        numerate += 1

    # print(rows)
    user_delete = int(input())
    row_sel = session.query(Table).filter(Table.id.startswith(user_delete)).all()
    if len(row_sel) == 0:
        print("Nothing to delete")
    else:
        specific_row = row_sel[0]
        session.delete(specific_row)
        session.commit()
        print("The task has been deleted!")
    pass


# session.query(Table).delete()

print("""1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit""")

user_choice = input()
while user_choice != "0":
    if user_choice == "1":
        rows = session.query(Table).all()
        # first_row = rows[0]
        # print(len(rows))
        if len(rows) > 0:
            print()
            today = datetime.today()
            print("Today " + str(today.day) + " " + str(today.strftime('%b') + ":"))
            start = 0
            for i in rows:
                print(str(start+1) + ".", rows[start])
                start += 1
            print()
        else:
            print()
            print("Today:")
            print("Nothing to do!")
            print()
    elif user_choice == "2":
        # rows = session.query(Table).all()
        today = datetime.today()
        day_count = 0
        while day_count != 7:
            day_increment = today + timedelta(days=day_count)
            day_week = check_day(day_increment.weekday())
            rows = session.query(Table).filter(Table.date_field == day_increment.date()).all()
            if len(rows) > 0:
                print(day_week + " " + str(day_increment.day) + " " + str(day_increment.strftime('%b') + ":"))
                start = 0
                for i in rows:
                    print(str(start + 1) + ".", rows[start])
                    start += 1
            else:
                print(day_week + " " + str(day_increment.day) + " " + str(day_increment.strftime('%b') + ":"))
                print("Nothing to do!")
            print()
            day_count += 1
    elif user_choice == "3":
        print("All tasks:")
        all_tasks()
        print()
    elif user_choice == "4":
        missed_tasks()
    elif user_choice == "5":
        print("Enter task")
        user_task = input()
        print("Enter deadline")
        user_deadline = input()
        new_row = Table(string_field=user_task, date_field=datetime.strptime(user_deadline, '%Y-%m-%d').date())
        session.add(new_row)
        session.commit()
        print("The task has been added!")
    elif user_choice == "6":
        delete_tasks()
        print()

    print("1) Today's tasks")
    print("2) Week's tasks")
    print("3) All tasks")
    print("4) Missed tasks")
    print("5) Add task")
    print("6) Delete task")
    print("0) Exit")
    user_choice = input()

print()
print("Bye!")