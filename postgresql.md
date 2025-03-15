SELECT
s.register_no, s.name, s.course, s.school, s.course_duration,
jsonb_agg(
jsonb_build_object(
'semester_no', sem.semester_no,
'exam_schedule_timetable_id', sem.exam_schedule_timetable_id,
'result_status', sem.result_status,
'sgpa', sem.sgpa,
'subjects', (
SELECT jsonb_agg(
jsonb_build_object(
'subject_code', sub.subject_code,
'subject_name', sub.subject_name,
'internal_marks', sub.internal_marks,
'external_marks', sub.external_marks,
'grade', sub.grade
)
)
FROM subjects sub
WHERE sub.register_no = s.register_no
AND sub.exam_schedule_timetable_id = sem.exam_schedule_timetable_id
)
)
) AS semesters
FROM students s
LEFT JOIN semesters sem ON s.register_no = sem.register_no
GROUP BY s.register_no;

select \* from semesters where exam_schedule_timetable_id=1926

select \* from semesters where register_no='22DBCAD053' AND semester_no=2

CREATE VIEW subject_results AS
SELECT \*
FROM subjects
WHERE register_no = '22DBCAD053' AND semester_no = 2;

SELECT SUM(credits_obtained \* grade_point) / SUM(credits_obtained) AS SGPA
FROM subjects
WHERE semester_no = 1 AND grade_point != 0;

SELECT SUM(sgpa \* earned_credits) / SUM(earned_credits) AS CGPA
FROM semesters
WHERE result_status = 'Successful' AND register_no='22DBCAD053';

WITH SuccessfulSemesters AS (
SELECT DISTINCT semester_no
FROM semesters
WHERE register_no = '22DBCAD053' AND result_status = 'Successful'
),
AllSemesters AS (
SELECT DISTINCT semester_no
FROM semesters
WHERE register_no = '22DBCAD053'
)
SELECT
CASE
WHEN (SELECT COUNT(_) FROM AllSemesters) = (SELECT COUNT(_) FROM SuccessfulSemesters)
THEN (SELECT SUM(sgpa \* earned_credits) / SUM(earned_credits)
FROM semesters
WHERE register_no = '22DBCAD053' AND result_status = 'Successful')
ELSE NULL
END AS CGPA;
