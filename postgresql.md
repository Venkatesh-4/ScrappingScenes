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

select * from semesters where exam_schedule_timetable_id=1926

select * from semesters where register_no='22DBCAD053' AND semester_no=2

select * from subject_results where grade Not like 'F%'