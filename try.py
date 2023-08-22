# 1
# select groups.group_name , count(students.group_name)
# from groups
# left join students on groups.group_name = students.group_name
# group by groups.group_name
# order by count(students.group_name) asc
# limit 1;

#2
# select students.first_name,students.last_name, courses.course_name from student_course
# join courses on student_course.course_id=courses.course_id
# join students on student_course.student_id=students.student_id
# where course_name = 'math';

# 3
# insert into  students (student_id, first_name, last_name, group_name)
# values (255, 'dima', 'sukleta', 'LC-13');


# 4

# 5
# insert into student_course (student_id, course_id)
# select students.student_id, courses.course_id
# from students, courses
# where students.student_id = '255'
# and courses.course_name in ('Math', 'Science');

# 6
# delete from student_course
# where student_course.student_id in (
# select * from (select students.student_id from student_course
# 		inner join students on student_course.student_id = students.student_id
# 		inner join courses on student_course.course_id = courses.course_id
# 		where students.student_id = 200 and courses.course_name = 'Art') as subquery);

