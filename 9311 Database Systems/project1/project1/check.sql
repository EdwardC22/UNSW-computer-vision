-- COMP9311 19s1 Project 1 Check
--
-- MyMyUNSW Check

create or replace function
	proj1_table_exists(tname text) returns boolean
as $$
declare
	_check integer := 0;
begin
	select count(*) into _check from pg_class
	where relname=tname and relkind='r';
	return (_check = 1);
end;
$$ language plpgsql;

create or replace function
	proj1_view_exists(tname text) returns boolean
as $$
declare
	_check integer := 0;
begin
	select count(*) into _check from pg_class
	where relname=tname and relkind='v';
	return (_check = 1);
end;
$$ language plpgsql;

create or replace function
	proj1_function_exists(tname text) returns boolean
as $$
declare
	_check integer := 0;
begin
	select count(*) into _check from pg_proc
	where proname=tname;
	return (_check > 0);
end;
$$ language plpgsql;

-- proj1_check_result:
-- * determines appropriate message, based on count of
--   excess and missing tuples in user output vs expected output

create or replace function
	proj1_check_result(nexcess integer, nmissing integer) returns text
as $$
begin
	if (nexcess = 0 and nmissing = 0) then
		return 'correct';
	elsif (nexcess > 0 and nmissing = 0) then
		return 'too many result tuples';
	elsif (nexcess = 0 and nmissing > 0) then
		return 'missing result tuples';
	elsif (nexcess > 0 and nmissing > 0) then
		return 'incorrect result tuples';
	end if;
end;
$$ language plpgsql;

-- proj1_check:
-- * compares output of user view/function against expected output
-- * returns string (text message) containing analysis of results

create or replace function
	proj1_check(_type text, _name text, _res text, _query text) returns text
as $$
declare
	nexcess integer;
	nmissing integer;
	excessQ text;
	missingQ text;
begin
	if (_type = 'view' and not proj1_view_exists(_name)) then
		return 'No '||_name||' view; did it load correctly?';
	elsif (_type = 'function' and not proj1_function_exists(_name)) then
		return 'No '||_name||' function; did it load correctly?';
	elsif (not proj1_table_exists(_res)) then
		return _res||': No expected results!';
	else
		excessQ := 'select count(*) '||
			   'from (('||_query||') except '||
			   '(select * from '||_res||')) as X';
		-- raise notice 'Q: %',excessQ;
		execute excessQ into nexcess;
		missingQ := 'select count(*) '||
				'from ((select * from '||_res||') '||
				'except ('||_query||')) as X';
		-- raise notice 'Q: %',missingQ;
		execute missingQ into nmissing;
		return proj1_check_result(nexcess,nmissing);
	end if;
	return '???';
end;
$$ language plpgsql;

-- proj1_rescheck:
-- * compares output of user function against expected result
-- * returns string (text message) containing analysis of results

create or replace function
	proj1_rescheck(_type text, _name text, _res text, _query text) returns text
as $$
declare
	_sql text;
	_chk boolean;
begin
	if (_type = 'function' and not proj1_function_exists(_name)) then
		return 'No '||_name||' function; did it load correctly?';
	elsif (_res is null) then
		_sql := 'select ('||_query||') is null';
		-- raise notice 'SQL: %',_sql;
		execute _sql into _chk;
		-- raise notice 'CHK: %',_chk;
	else
		_sql := 'select ('||_query||') = '||quote_literal(_res);
		-- raise notice 'SQL: %',_sql;
		execute _sql into _chk;
		-- raise notice 'CHK: %',_chk;
	end if;
	if (_chk) then
		return 'correct';
	else
		return 'incorrect result';
	end if;
end;
$$ language plpgsql;

-- check_all:
-- * run all of the checks and return a table of results

drop type if exists TestingResult cascade;
create type TestingResult as (test text, result text);

create or replace function
	check_all() returns setof TestingResult
as $$
declare
	i int;
	testQ text;
	result text;
	out TestingResult;
	tests text[] := array['q1', 'q2', 'q3', 'q4', 'q5','q6','q7','q8','q9','q10','q11','q12'];
begin
	for i in array_lower(tests,1) .. array_upper(tests,1)
	loop
		testQ := 'select check_'||tests[i]||'()';
		execute testQ into result;
		out := (tests[i],result);
		return next out;
	end loop;
	return;
end;
$$ language plpgsql;


--
-- Check functions for specific test-cases in Project 1
--

create or replace function check_q1() returns text
as $chk$
select proj1_check('view','q1','q1_expected',
				   $$select * from q1$$)
$chk$ language sql;

create or replace function check_q2() returns text
as $chk$
select proj1_check('view','q2','q2_expected',
				   $$select * from q2$$)
$chk$ language sql;

create or replace function check_q3() returns text
as $chk$
select proj1_check('view','q3','q3_expected',
				   $$select * from q3$$)
$chk$ language sql;

create or replace function check_q4() returns text
as $chk$
select proj1_check('view','q4','q4_expected',
				   $$select * from q4$$)
$chk$ language sql;

create or replace function check_q5() returns text
as $chk$
select proj1_check('view','q5','q5_expected',
				   $$select * from q5$$)
$chk$ language sql;

create or replace function check_q6() returns text
as $chk$
select proj1_check('view','q6','q6_expected',
				   $$select * from q6$$)
$chk$ language sql;

create or replace function check_q7() returns text
as $chk$
select proj1_check('view','q7','q7_expected',
				   $$select * from q7$$)
$chk$ language sql;

create or replace function check_q8() returns text
as $chk$
select proj1_check('view','q8','q8_expected',
				   $$select * from q8$$)
$chk$ language sql;

create or replace function check_q9() returns text
as $chk$
select proj1_check('view','q9','q9_expected',
				   $$select * from q9$$)
$chk$ language sql;

create or replace function check_q10() returns text
as $chk$
select proj1_check('view','q10','q10_expected',
				   $$select * from q10$$)
$chk$ language sql;

create or replace function check_q11() returns text
as $chk$
select proj1_check('view','q11','q11_expected',
				   $$select * from q11$$)
$chk$ language sql;

create or replace function check_q12() returns text
as $chk$
select proj1_check('view','q12','q12_expected',
				   $$select * from q12$$)
$chk$ language sql;

create or replace function check_q13() returns text
as $chk$
select proj1_check('function','q13','q13_expected',
				   $$select * from q13(661)$$)
$chk$ language sql;


drop table if exists q1_expected;
create table q1_expected (
   subject_longname LongName, 
   subject_num integer
);


drop table if exists q2_expected;
create table q2_expected (
	 orgunit_id   integer ,
	 orgunit      mediumstring,
	 orgunit_type shortname ,
	 program       longname 
);

drop table if exists q3_expected;
create table q3_expected (
	 course      integer ,          
	 student_num bigint  ,                        
	 avg_mark    numeric(4,2) 
);

drop table if exists q4_expected;
create table q4_expected (
	student_num bigint 
);

drop table if exists q5_expected;
create table q5_expected (
	 unswid    integer,                      
	 min_mark  integer,                      
	 course    integer            
);

drop table if exists q6_expected;
create table q6_expected (
  course_id  integer
);

drop table if exists q7_expected;
create table q7_expected (
	staff_name  longname,                      
	semester    longname,                      
	course_num  bigint  
);

drop table if exists q8_expected;
create table q8_expected (
	role_id       integer ,                        
	role_name     longstring ,                     
	num_students  bigint     
);

drop table if exists q9_expected;
create table q9_expected (
	year          courseyeartype,                         
	term          character(2),                         
	stype  character varying(5),                    
	average_mark  numeric                  
);

drop table if exists q10_expected;
create table q10_expected (
	room longname,
	capacity integer,
	num integer
);

drop table if exists q11_expected;
create table q11_expected (
	staff longname,
	subject longname,
	num integer
);

drop table if exists q12_expected;
create table q12_expected (
	staff longname,
	role longname,
	hd_rate numeric(4,2) 
);

drop table if exists q13_expected;
create table q13_expected (
		unswid integer, 
	name text, 
	roles text
);




COPY q1_expected (subject_longname, subject_num) FROM stdin;
Combined PhD Thesis Full Time	2
Combined PhD Thesis Full-Time	7
Combined PhD Thesis Part-Time	3
PhD F/T Cross-faculty	4
PhD P/T Cross-faculty	5
PhD Research Thesis Full-Time	3
PhD Research Thesis Part-Time	3
PhD Thesis Combined Full Time	3
PhD Thesis Combined Full-Time	5
PhD Thesis Combined Part Time	4
\.

-- ( )+\|+( )+
COPY q2_expected (OrgUnit_id, OrgUnit, OrgUnit_type, Program) FROM stdin;
183	Faculty of Medicine	Faculty	Arts / Medicine
183	Faculty of Medicine	Faculty	Science/Medicine
183	Faculty of Medicine	Faculty	Arts/Medicine
165	School of Law	School	Engineering / Law
165	School of Law	School	Social Work / Law
183	Faculty of Medicine	Faculty	Arts/Medicine
164	Faculty of Law	Faculty	Architecture / Law
164	Faculty of Law	Faculty	Planning/Law
\.

COPY q3_expected (course,student_num,avg_mark) FROM stdin;
25634	13	71.00
26632	16	71.13
27293	18	76.39
32256	13	73.77
35083	11	78.45
39264	41	70.34
41429	35	74.66
42097	19	74.58
42365	33	70.52
42928	63	73.13
44532	14	77.07
45449	18	70.89
47225	11	76.27
47228	32	71.53
48519	51	71.88
50604	11	77.09
52545	31	74.61
52896	47	70.94
56159	26	74.00
56166	28	76.11
56658	18	72.44
56686	29	73.28
57754	12	76.58
58136	12	70.58
58646	12	71.92
59444	26	71.81
60624	20	71.80
61151	30	71.50
63081	20	73.30
63110	16	73.75
63116	21	75.00
63393	23	76.48
63616	18	71.78
63646	18	77.00
66503	26	75.04
66740	23	76.17
66777	38	71.66
67145	59	75.69
67173	23	76.78
\.

COPY q4_expected (student_num) FROM stdin;
431
\.


COPY q5_expected (unswid, min_mark, course) FROM stdin;
50406779	86	58768
50404334	76	52006
50405775	73	55572
50405314	70	58915
50402823	66	44898
50412699	66	62494
50415954	66	51968
50415059	57	60813
50500010	57	60813
50500023	30	58770
\.

COPY q6_expected (course_id) FROM stdin;
39873
39920
40204
40431
40503
40663
40664
40832
40877
40945
40967
41223
41305
41377
41428
41947
42079
42296
42538
42610
42693
42896
42920
42968
43044
43048
43065
43069
43177
43248
43281
43424
43426
43507
43522
43619
43874
44057
44102
44103
44118
44136
44181
44380
44381
44442
44585
44589
44595
44758
44999
45000
45028
45040
45094
45306
45336
45648
45876
45898
45911
45954
45981
45983
46167
46257
46276
46760
46784
46999
47294
47363
47419
47679
47686
47769
47804
47852
47856
47940
47960
48002
48018
48223
48228
48293
48369
48436
48447
48449
48646
48800
48965
49026
49209
49239
49254
49257
49302
49329
49376
49390
49437
49485
49571
49582
49590
49604
49606
49638
49801
49830
49836
49878
50049
50058
50273
50329
50437
50557
50737
50840
50843
50946
51029
51081
51124
51141
51238
51304
51321
51425
51497
51505
51833
51928
52210
52272
52500
52642
52741
52780
52870
53153
53162
53248
53404
53510
53681
53700
\.

COPY q7_expected (staff_name, semester, course_num) FROM stdin;
Peter Murray	Semester 1 2006	2
Douglas Duffy	Semester 1 2006	2
Paul Hogben	Semester 1 2006	2
Richard Buckland	Semester 1 2006	2
Michael Burton	Semester 1 2006	2
Phaik-Ee Lim	Semester 1 2006	2
Yinong Xu	Semester 2 2006	2
Nick Roberts	Semester 2 2006	2
Carl Reidsema	Semester 2 2006	2
Peter Graham	Semester 2 2006	2
Peter Murray	Semester 2 2006	2
Lesley Ulman	Semester 2 2006	2
Jennifer Jordan	Summer Semester 2007	1
Karin Banna	Summer Semester 2007	1
Mahiuddin Chowdhury	Asia Semester March 2007	3
Steve King	Asia Semester March 2007	3
Michael Edwards	Asia Semester March 2007	3
Dennis Isbister	Asia Semester August 2007	3
Frances Miley	Asia Semester August 2007	3
\.

COPY q8_expected (role_id, role_name, num_students) FROM stdin;
1870	Course Convenor	1648
3003	Course Lecturer	1028
3004	Course Tutor	189
\.


COPY q9_expected (year, term, stype, average_mark) FROM stdin;
2003	S2	intl	82.00
2003	S2	local	64.00
2004	S2	intl	69.33
2005	S1	intl	78.00
2005	S1	local	76.00
2006	S2	intl	62.00
2007	S1	intl	90.00
2008	S1	intl	52.00
2009	S1	intl	55.00
2011	S1	intl	73.43
2011	S1	local	64.50
2012	S1	intl	75.00
2012	S1	local	75.00
\.

COPY q10_expected (room, capacity, num) FROM stdin;
Sir John Clancy Auditorium	1000	10
Matthews Theatre A	500	17
Keith Burrows Theatre	400	16
Matthews Theatre B	300	17
Webster Theatre B	200	17
Webster Theatre A	200	17
Biomedical Lecture Theatre B	200	17
Biomedical Lecture Theatre C	200	17
Biomedical Lecture Theatre D	200	17
Biomedical Lecture Theatre A	200	17
Macauley Theatre	200	17
OMB-112	185	17
Central Lecture Block Theatre 5	150	12
Central Lecture Block Theatre 2	150	12
Central Lecture Block Theatre 3	150	12
Central Lecture Block Theatre 4	150	12
Central Lecture Block Theatre 1	150	12
CE-101	113	 7
AS-G05	108	 6
Matthews Theatre D	100	15
\.


COPY q11_expected (staff, subject, num) FROM stdin;
Muriel Watt	Sustainability Assessment and Risk Analysis	34
Arthur Ramer	Foundations of Computer Science	13
Arthur Ramer	Engineering Decision Structures	114
Obada Kayali	Engineering Materials	44
Obada Kayali	Sustainability of Concrete Structures	5
Obada Kayali	Concrete and Prestressed Concrete Structures	6
\.


COPY q12_expected (staff, role, hd_rate) FROM stdin;
Anna Munster	Course Convenor	0.09
Anna Munster	Course Lecturer	0.04
Anna Munster	Course Tutor	0.03
Helen Gibbon	Course Convenor	0.06
Helen Gibbon	Course Lecturer	0.11
Helen Gibbon	Course Tutor	0.06
John Peterson	Course Convenor	0.13
John Peterson	Course Lecturer	0.08
John Peterson	Course Tutor	0.19
Maria Nurhayati	Course Convenor	0.27
Maria Nurhayati	Course Lecturer	0.24
Maria Nurhayati	Course Tutor	0.04
Michael Wearing	Course Convenor	0.12
Michael Wearing	Course Lecturer	0.08
Michael Wearing	Course Tutor	0.08
\.


COPY q13_expected (unswid, name, roles) FROM stdin;
3140956	Thomas Loveday	Senior Lecturer, Architecture Program (2011-09-05..2011-09-05)\nSenior Lecturer, Interior Architecture Program (2011-11-25..)\n
9226425	Stephen Ward	Program Head, Industrial Design Program (2001-01-01..2011-09-27)\nLecturer, Industrial Design Program (2011-09-27..)\n
\.
