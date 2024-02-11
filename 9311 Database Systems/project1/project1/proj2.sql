-- comp9311 21T1 Project 1 plpgsql part
--
-- MyMyUNSW Solutions


-- Q13:
create type EmploymentRecord as (unswid integer, staff_name text, roles text);
create or replace function Q13(integer) 
	returns setof EmploymentRecord 
as $$
... one SQL statement, possibly using other functions defined by you ...
$$ language plpgsql;