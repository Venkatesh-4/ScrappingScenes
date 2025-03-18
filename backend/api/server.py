from fastapi import FastAPI
import asyncpg
app = FastAPI()

async def get_db_connection():
    return await asyncpg.connect(
        database="cmr_student_database",  # Change "dbname" to "database"
        user="postgres",
        password="venkatesh",
        host="localhost",
        port="5432" 
    )

@app.get("/students")
async def get_students():
    query = """
    SELECT 
    s.register_no, s.name, s.cgpa, s.course, s.school, s.course_duration,
    jsonb_agg(
        jsonb_build_object(
			'exam_schedule_timetable_id', sem.exam_schedule_timetable_id,
            'semester_no', sem.semester_no,
			'result_status', sem.result_status,
			'block_status', sem.block_status,
			'block_reason', sem.block_reason,
			'ordinance', sem.ordinance,
            'passing_year', sem.passing_year,
			'passing_month', sem.passing_month,
            'sgpa', sem.sgpa,
			'total_credits', sem.total_credits,
			'earned_credits', sem.earned_credits,
			'obtained_marks', sem.obtained_marks,
			'out_of_marks', sem.out_of_marks,
            'subjects', (
                SELECT jsonb_agg(
                    jsonb_build_object(
                        'subject_code', sub.subject_code,
                        'subject_name', sub.subject_name,
                        'internal_marks', sub.internal_marks,
						'internal_passing_marks', sub.internal_passing_marks,
						'max_internal_marks', sub.max_internal_marks,
                        'external_marks', sub.external_marks,
						'external_passing_marks', sub.external_passing_marks,
						'max_external_marks', sub.max_external_marks,
                        'grade', sub.grade,
						'grade_point', sub.grade_point,
						'credits_obtained', sub.credits_obtained,
						'max_credits', sub.max_credits
                    )
                ) 
                FROM subjects sub 
                WHERE sub.register_no = s.register_no 
                AND sub.semester_no = sem.semester_no
                )
            )
        ) AS semesters
    FROM students s
    LEFT JOIN semesters sem ON s.register_no = sem.register_no
    GROUP BY s.register_no;
    """
    conn = await get_db_connection()
    rows = await conn.fetch(query)
    await conn.close()
    return rows
