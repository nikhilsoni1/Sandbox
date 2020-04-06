select count(distinct(conversation_id)) from Conversation_table
where session_start.year = '2019' and session_start.month=1

--------------

with foo as (
        SELECT * FROM Conversation_table x1 inner join Agent_table x2 on x1.agent_id = x2.agent_id
        where x2.vendor = 'Vendor_1'
)

select distinct(conversation_id), count(session_id) as freq as pa from foo
group by conversation_id
order by freq desc limit 1

--------------

with foo as (
        SELECT * FROM Conversation_table x1 inner join Agent_table x2 on x1.agent_id = x2.agent_id
        where x1.session_start.year = '2019' and x1.session_start_month = '1'
)

with foo1 as(select conversation_id, conversation_end, vendor from foo order by conversation_end desc)

with foo2 as (select vendor, count(conversation_id) as freq from foo1
                group by vendor
                having conversation_end = max(conversation_end)
              )
select * from foo2 order by freq desc limit 1

--------------



