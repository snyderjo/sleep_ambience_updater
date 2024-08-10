with lastSunday as
(
    select current_date - extract(dow from current_date)::integer as baseday
    )
,
bounds as
(
    select
        (baseday - interval'2 weeks') + time'12:00' as upper_bound
        , (baseday - interval'3 weeks') + time'12:00' as lower_bound
    from lastSunday
)
,
ambience_recs as (
    select a.reading_id,a.reading_dttm, a.temp, a.pressure, a.humidity
    from ambience.readings a
    right join ambience.location b
        on a.location_id = b.id
    where 1 = 1
        and room = 'bed'
        and active
        and reading_dttm > (select lower_bound from bounds)
        and reading_dttm < (select upper_bound from bounds)
    order by reading_dttm
)
select * from ambience_recs;