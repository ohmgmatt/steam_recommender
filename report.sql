SELECT 'Distinct Users' as 'Category', COUNT(DISTINCT steamid) FROM gameplay
UNION
SELECT 'Distinct Apps', COUNT(DISTINCT appid) FROM gameplay
UNION
SELECT 'Total Rows', COUNT(*) FROM gameplay
UNION
SELECT 'IDs to Parse', COUNT(*) FROM parse_id
UNION
SELECT 'FInished IDs', COUNT(*) FROM finished_id;
