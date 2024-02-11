-- comp9311 21T1 Project 1 plpgsql part
--Ruohao Chen
--z5111287
-- MyMyUNSW Solutions


-- Q13:

-- trying to locate all the organization i.e. find the org->sub-org->sub-org
-- but do not know how to transfer them into a plpgsql function

--with recursive r as ( 
--     select member from orgunit_groups where owner = $1
--     union   ALL 
--      select orgunit_groups.member from orgunit_groups, r where orgunit_groups.owner = r.member 
--    ) select * from r;


create type staff_count as (unswid integer);

create or replace function
	Q13_staff_filter(integer) returns setof staff_count
as
$$
begin
	return query
	select	distinct people.unswid
	from people, affiliations, orgunits, staff_roles, orgunit_groups
	where people.id = affiliations.staff
		and affiliations.orgunit = orgunits.id
		and affiliations.role = staff_roles.id
		and orgunits.id = orgunit_groups.member
 		and orgunit_groups.owner = $1
	group by people.unswid
	having count(people.unswid) > 1;
end;
$$ language plpgsql;

create type Q13_select as (unswid integer, name text, roles text, prog text, starting date, ending date);

create or replace function Q13_data_filter(integer)
	returns setof Q13_select 
as $$

declare
role1 	Q13_select;
role2	Q13_select;

begin
	for role1 in 
		select distinct people.unswid,
				cast(people.name as text),
				cast(staff_roles.name as text),
				cast(orgunits.name as text),
				cast(affiliations.starting as date),
				cast(affiliations.ending as date)
		from people, affiliations, orgunits, staff_roles, orgunit_groups, (select * from Q13_staff_filter($1)) as Q13_staff_filter
		where people.id = affiliations.staff
			and affiliations.orgunit = orgunits.id
			and affiliations.role = staff_roles.id
			and orgunits.id = orgunit_groups.member
			and people.unswid = Q13_staff_filter.unswid
	loop
		for role2 in
			select distinct people.unswid,
				cast(people.name as text),
				cast(staff_roles.name as text),
				cast(orgunits.name as text),
				cast(affiliations.starting as date),
				cast(affiliations.ending as date)
		from people, affiliations, orgunits, staff_roles, orgunit_groups, (select * from Q13_staff_filter($1)) as Q13_staff_filter
		where people.id = affiliations.staff
			and affiliations.orgunit = orgunits.id
			and affiliations.role = staff_roles.id
			and orgunits.id = orgunit_groups.member
			and people.unswid = Q13_staff_filter.unswid
			and people.unswid = role1.unswid
		loop
			if role2.starting >= role1.ending or role2.ending <= role1.starting then
				return next role2;
			end if;
		end loop;
	end loop;	
end;
$$ language plpgsql;

create type EmploymentRecord as (unswid integer, name text, roles text);

create or replace function Q13(integer)
    returns setof EmploymentRecord 
as $$
declare
    r EmploymentRecord; 
    row2 Q13_select;
    row1 Q13_select;
    roles text := '';
begin
for row2 in 
	select distinct * from Q13_data_filter($1)
	order by Q13_data_filter.name desc, Q13_data_filter.starting
loop
    if row1 is null then 
        row1 := row2;
    end if;

    if row1.unswid = row2.unswid then 
        r.unswid := row2.unswid;
        r.name := row2.name;
        if row2.ending is not null then 
            roles := roles||row2.roles||', '||row2.prog||' ('||row2.starting::text||'..'||row2.ending::text||')'||chr(10);
            r.roles = roles;
        end if;
        if row2.ending is null then
            roles := roles||row2.roles||', '||row2.prog||' ('||row2.starting::text||'..'||')'||chr(10);
            r.roles = roles;
        end if;
    end if;

    if row1.unswid != row2.unswid then 
        r.roles = roles;
        roles := '';
		return next r; 
		roles := roles||row2.roles||', '||row2.prog||' ('||row2.starting::text||'..'||row2.ending::text||')'||chr(10);
		r.unswid := row2.unswid;
        r.name := row2.name;
    end if;
    row1 := row2;
end loop;
r.roles = roles;
return next r;
end;
$$ language plpgsql;
