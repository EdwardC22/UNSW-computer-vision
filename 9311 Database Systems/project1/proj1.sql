-- comp9311 21T1 Project 1 sql part
-- Ruohao Chen
-- z5111287
-- MyMyUNSW Solutions


-- Q1:
create or replace view Q1(subject_longname, subject_num)
as
--... SQL statements, possibly using other views/functions defined by you ...
select subjects.longname,count(subjects.id)
from subjects
where subjects.longname like'%PhD%'
group by subjects.longname
having count(subjects.id) > 1
;

-- Q2:
create or replace view Q2(OrgUnit_id, OrgUnit, OrgUnit_type, Program)
as
--... SQL statements, possibly using other views/functions defined by you ...
select OrgUnits.id, OrgUnits.name, OrgUnit_types.name, Programs.name
from orgunits 
     join programs on (programs.offeredby = orgunits.id) 
     join OrgUnit_types on (OrgUnit_types.id = orgunits.utype)
where programs.uoc > 300
;

-- Q3:
create or replace view Q3_course(course_id,student_num,avg_mark) as
select courses.id, count(course_enrolments.student), avg(course_enrolments.mark)::numeric(4,2)
from course_enrolments, courses
where course_enrolments.course = courses.id
    and course_enrolments.mark is not null
group by courses.id
having count(course_enrolments.mark) > 10
    and avg(course_enrolments.mark) > 70
;

create or replace view Q3_only(course)
as
select courses.id
from courses, course_staff, staff_roles
where courses.id = course_staff.course
    and staff_roles.id = course_staff.role
group by courses.id
having count (distinct staff_roles.id) = 1
;

create or replace view Q3(course,student_num,avg_mark)
as 
--... SQL statements, possibly using other views/functions defined by you ...
select distinct Q3_course.course_id, Q3_course.student_num, Q3_course.avg_mark
from Q3_course, Q3_only, course_staff, staff_roles
where Q3_only.course = Q3_course.course_id
    and Q3_only.course = course_staff.course
    and course_staff.role = staff_roles.id
    and staff_roles.name = 'Course Tutor'
;

-- Q4:
create or replace view Q4_courses(course_id)
as
select course_enrolments.course
from course_enrolments
    join classes on (classes.course = course_enrolments.course)
    join class_types on (class_types.id = classes.ctype)
    join rooms on (rooms.id = classes.room)
    join buildings on (buildings.id = rooms.building)
where Class_types.name = 'Lecture'
    and Buildings.name in ('Quadrangle', 'Red Centre')
group by  course_enrolments.course
having count(distinct Buildings.name) = 2
;

create or replace view Q4(student_num)
as
--... SQL statements, possibly using other views/functions defined by you ...
select count(distinct course_enrolments.student)
from course_enrolments
    join Q4_courses on (course_id = course_enrolments.course);
;
--Q5:
create or replace view Q5_marks(staff, min_mark, course)
as
select staff.id, min(Course_enrolments.mark), Courses.id
from staff, Course_enrolments, Courses, course_staff, OrgUnits, subjects
where course_staff.staff = staff.id
    and course_enrolments.course = courses.id
    and course_staff.course = courses.id
    and courses.subject = subjects.id
    and subjects.offeredby = orgunits.id
    and OrgUnits.name = 'School of Law'
    and course_enrolments.mark is not null
group by staff.id, Courses.id
order by staff.id
;

create or replace view Q5_min_marks(unswid, mark)
as 
select Q5_marks.staff, min(Q5_marks.min_mark)
from Q5_marks
group by Q5_marks.staff
;

create or replace view Q5(unswid, min_mark, course)
as
--... SQL statements, possibly using other views/functions defined by you ...
select Q5_min_marks.unswid, Q5_min_marks.mark, Q5_marks.course
from Q5_marks, Q5_min_marks
where Q5_min_marks.mark = Q5_marks.min_mark
    and Q5_min_marks.unswid = Q5_marks.staff
order by Q5_min_marks.mark desc
;

-- Q6:
create or replace view Q6_course (course, avg_mark)
as
select course_enrolments.course, avg(course_enrolments.mark)
from course_enrolments
    join courses on (courses.id = course_enrolments.course )
    join semesters on (courses.semester = semesters.id)
where course_enrolments.mark is not null 
    and semesters.year in ('2009','2010')
group by course_enrolments.course
having count(student) > 10
;

create or replace view Q6_over_avg_mark(course,student_num)
as
select Q6_course.course, count(course_enrolments.student)
from Q6_course
    join course_enrolments on (Q6_course.course = course_enrolments.course)
where course_enrolments.mark > Q6_course.avg_mark
group by Q6_course.course
;

create or replace view Q6(course_id)
as
--... SQL statements, possibly using other views/functions defined by you ...
select Q6_over_avg_mark.course
from Q6_over_avg_mark
    join course_enrolments on (course_enrolments.course = Q6_over_avg_mark.course)
where course_enrolments.mark is not null
group by Q6_over_avg_mark.course, Q6_over_avg_mark.student_num
having Q6_over_avg_mark.student_num < 0.4* count (course_enrolments.student)
;

-- Q7:
create or replace view Q7_course(staff, semester, course)
as
select course_staff.staff, semesters.longname, courses.id
from course_staff, courses, semesters, course_enrolments
where course_staff.course = courses.id
    and courses.semester = semesters.id
    and course_enrolments.course = courses.id
    and semesters.year in ('2005','2006','2007')
group by course_staff.staff, semesters.id, courses.id
having count (course_enrolments.student) >= 20
order by course_staff.staff
;

create or replace view Q7_count_course(staff, semester, course_num)
as
select staff, semester, count(course)
from Q7_course
group by staff, semester
;

create or replace view Q7_max_course(semester, course_num)
as
select semester, max (course_num)
from Q7_count_course
group by semester
;

create or replace view Q7(staff_name, semester, course_num)
as
--... SQL statements, possibly using other views/functions defined by you ...
select people.name, Q7_max_course.semester,Q7_max_course.course_num
from Q7_count_course, people, Q7_max_course
where Q7_count_course.staff = people.id
    and Q7_count_course.course_num = Q7_max_course.course_num
    and Q7_max_course.semester = Q7_count_course.semester
;

-- Q8: 
create or replace view Q8_org(role_id, role_name, student)
as
select staff_roles.id, staff_roles.name, Course_enrolments.student
from staff_roles
    join course_staff on (course_staff.role = staff_roles.id)
    join courses on (courses.id = course_staff.course)
    join course_enrolments on (course_enrolments.course = courses.id)
    join affiliations on (affiliations.staff = course_staff.staff)
    join orgunits on (orgunits.id = affiliations.orgunit)
    join semesters on (semesters.id = courses.semester)
where semesters.year = '2010'
    and orgunits.longname = 'School of Computer Science and Engineering'
;
create or replace view Q8(role_id, role_name, num_students)
as
--... SQL statements, possibly using other views/functions defined by you ...
select role_id, role_name, count(distinct student)
from Q8_org
group by role_id, role_name
;

-- Q9:
create or replace view Q9(year, term, stype, average_mark)
as
--... SQL statements, possibly using other views/functions defined by you ...
select semesters.year, semesters.term, students.stype, avg(course_enrolments.mark)::numeric(4,2)
from semesters
    join courses on (courses.semester = semesters.id)
    join course_enrolments on (course_enrolments.course = courses.id)
    join students on (course_enrolments.student = students.id)
    join subjects on (courses.subject = subjects.id)
where course_enrolments.mark is not null
    and subjects.name = 'Data Management'
group by semesters.year, semesters.term, students.stype
;

-- Q10:
create or replace view Q10_facility_num(room,capacity, num)
as
select Rooms.longname,Rooms.capacity, count(distinct room_facilities.facility)
from rooms 
    join room_facilities on (room_facilities.room = rooms.id)
where Rooms.capacity >= 100
    and room_facilities.facility is not null
group by Rooms.capacity,rooms.id
;
create or replace view Q10_max(capacity, num)
as
select capacity, max(num)
from Q10_facility_num
group by capacity
;
create or replace view Q10(room, capacity, num)
as
--... SQL statements, possibly using other views/functions defined by you ...
select Q10_facility_num.room, Q10_max.capacity, Q10_max.num
from Q10_facility_num, Q10_max
where Q10_max.capacity = Q10_facility_num.capacity
    and Q10_max.num = Q10_facility_num.num
;
-- Q11:
create or replace view Q11_table1(staff, course, subject, year)
as
select distinct course_staff.staff, courses.id, subjects.longname, semesters.year
from course_staff
    join courses on (courses.id = course_staff.course)
    join subjects on (courses.subject = subjects.id)
    join semesters on (courses.semester = semesters.id)
    join course_enrolments on (course_enrolments.course = courses.id)
where semesters.term in ('S1','S2')
    and course_staff.staff >= 5035400
    and course_staff.staff <= 5035499
order by course_staff.staff, semesters.year
;

create or replace view Q11_table2(staff, subject)
as
select distinct t1.staff, t1.subject
from Q11_table1 as t1
    inner join Q11_table1 as t2 on (t1.staff = t2.staff and t1.year + 1 = t2.year and t1.subject = t2.subject)
    inner join Q11_table1 as t3 on (t1.staff = t3.staff and t1.year + 2 = t3.year and t1.subject = t3.subject)
;

create or replace view Q11_table3(staff, subject, course, num)
as
select distinct Q11_table1.staff, Q11_table1.subject, Q11_table1.course, count (course_enrolments.mark)
from Q11_table1, Q11_table2, course_enrolments
where Q11_table1.staff = Q11_table2.staff
    and Q11_table1.subject = Q11_table2.subject
    and Q11_table1.course = course_enrolments.course
    and course_enrolments.mark is not null
group by Q11_table1.staff, Q11_table1.subject, Q11_table1.course
;
create or replace view Q11(staff, subject, num)
as
--... SQL statements, possibly using other views/functions defined by you ...
select people.name, Q11_table3.subject, max(Q11_table3.num)
from Q11_table3
    join People on (Q11_table3.staff = people.id)
group by people.name, Q11_table3.subject
;

-- Q12:
create or replace view Q12_subject_select(staff, subject_num)
as
select course_staff.staff, count (distinct courses.subject)
from course_staff,courses
where course_staff.course = courses.id
group by course_staff.staff
having count (distinct courses.subject) > 1 
;

create or replace view Q12_role_select(staff, subject)
as
select Q12_subject_select.staff, courses.subject
from Q12_subject_select, course_staff, courses, staff_roles
where Q12_subject_select.staff = course_staff.staff
    and course_staff.course = courses.id
    and course_staff.role = staff_roles.id
group by Q12_subject_select.staff, courses.subject
having count (distinct staff_roles.name) = 3
;

create or replace view Q12_staff(staff)
as
select staff
    from Q12_role_select
    group by staff
    having count(subject) >= 2
;

create or replace view Q12_select(staff,role)
as
select distinct Q12_staff.staff, staff_roles.name
from Q12_role_select, Q12_staff, course_staff, courses, staff_roles
where Q12_staff.staff = Q12_role_select.staff
    and Q12_role_select.subject = courses.subject
    and Q12_staff.staff = course_staff.staff
    and course_staff.course = courses.id
    and course_staff.role = staff_roles.id
;

create or replace view Q12_hd(staff, role, hd_num)
as
select people.name, staff_roles.name, count (course_enrolments.mark)
from course_staff, course_enrolments, Q12_select, staff_roles, people
where Q12_select.staff = course_staff.staff
    and course_staff.role = staff_roles.id
    and course_staff.course = course_enrolments.course
    and Q12_select.staff = people.id
    and course_enrolments.mark >= 85
group by people.name, staff_roles.name
;

create or replace view Q12_student(staff, role, student_num)
as
select people.name, staff_roles.name, count (course_enrolments.mark)
from course_staff, course_enrolments, Q12_select, staff_roles, people
where Q12_select.staff = course_staff.staff
    and course_staff.role = staff_roles.id
    and course_staff.course = course_enrolments.course
    and Q12_select.staff = people.id
    and course_enrolments.mark is not null
group by people.name, staff_roles.name
;

create or replace view Q12(staff, role, hd_rate)
as
--... SQL statements, possibly using other views/functions defined by you ...
select Q12_hd.staff, Q12_hd.role, CAST(Q12_hd.hd_num::numeric(20,4)/Q12_student.student_num as decimal(4,2))
from Q12_student, Q12_hd
where Q12_student.staff = Q12_hd.staff
    and Q12_student.role = Q12_hd.role
group by Q12_hd.staff, Q12_hd.role, Q12_hd.hd_num, Q12_student.student_num
;
