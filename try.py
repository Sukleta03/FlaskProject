from app.data import student_func, group_func, course_func, random_courses

name = student_func(200)
group = group_func(10)
course = course_func()


class Student(object):

    def __init__(self, first_name, last_name, group):
        self.first_name = first_name
        self.last_neme = last_name
        self.group = group

    courses_list = random_courses(course_func())

# firts = ['dima', 'anton']
# last = ['sukleta', 'subota']
# group = ['ПЕ-211', 'РА-203']


new_student = Student(first_name='dima', last_name='sukleta', group="ПЕ-211")

students_list = []
for i in range(2):
    first_name, lasy_name = name.split(" ")
    new_student = Student(first_name=first_name[i], last_name=last_name[i], group=group[i])
    students_list.append(new_student)

for j, student in enumerate(students_list):
    print(students_list[j].first_name)
    print(students_list[j].last_neme)
    print(students_list[j].group)
    print(students_list[j].courses_list)



# class StudentGroup(Base):
#     __tablename__ = 'student_group'
#
#     id = Column(String, primary_key=True)
#     student_id = Column(Integer, ForeignKey('students.student_id'), primary_key=True)
#     group_id = Column(Integer, ForeignKey('groups.group_id'), primary_key=True)
#
#     student = relationship("StudentModel", backref=backref("student_group", cascade="all"))
#     group = relationship("GroupModel", backref=backref("student_group", cascade="all"))
#
#     def __init__(self, student=None, group=None):
#         self.id = uuid.uuid4().hex
#         self.student = student
#         self.group = group

