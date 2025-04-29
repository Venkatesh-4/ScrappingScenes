from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
import asyncio
import sys
import subprocess
from pathlib import Path
from backend.database.db_connection_asyncpg import get_db_connection
from backend.scraper.fetcher import main as fetcher_main
import os
from pydantic import BaseModel

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Credentials(BaseModel):
    username: str
    password: str

@app.get("/students")
async def get_students():
    query = """
    SELECT 
    s.register_no, 
    s.name, 
    s.cgpa, 
    s.course, 
    s.school, 
    s.course_duration,
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
                WHERE 
                    sub.register_no = s.register_no 
                    AND sub.semester_no = sem.semester_no
                    AND sub.exam_schedule_timetable_id = sem.exam_schedule_timetable_id
            )
        )
    ) FILTER (WHERE sem.register_no IS NOT NULL) AS semesters
FROM students s
LEFT JOIN semesters sem ON s.register_no = sem.register_no
GROUP BY s.register_no;

    """
    conn = await get_db_connection()
    rows = await conn.fetch(query)
    await conn.close()
    return rows

@app.get("/sgpa_progression/{register_no}")
async def sgpa_progression(register_no: str):
    query = """
    SELECT semester_no, passing_year, passing_month, sgpa
    FROM semesters
    WHERE register_no = $1
    ORDER BY passing_year, passing_month, semester_no;
    """
    # AND sgpa is NOT NULL
    conn = await get_db_connection()
    rows = await conn.fetch(query, register_no)
    await conn.close()
    return [{"semester": r["semester_no"], "year": r["passing_year"], "month": r["passing_month"], "sgpa": r["sgpa"]} for r in rows]

@app.post("/api/run-fetcher")
async def run_fetcher(credentials: Credentials):
    try:
        # Use the same Python executable that's running this FastAPI app
        python_executable = sys.executable
        
        # Set up environment with UTF-8 encoding
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"
        
        # Run the fetcher script using the virtual environment's Python
        result = subprocess.run(
            [python_executable, "-c", 
             f"from backend.scraper.fetcher import main; main('{credentials.username}', '{credentials.password}')"],
            capture_output=True,
            text=True,
            check=True,
            cwd=str(Path(__file__).parent.parent.parent),  # Run from project root
            env=env
        )
        
        return {
            "output": result.stdout,
            "error": result.stderr,
            "success": True
        }
        
    except subprocess.CalledProcessError as e:
        return {
            "output": e.stdout,
            "error": e.stderr,
            "success": False
        }
    except Exception as e:
        return {
            "output": "",
            "error": str(e),
            "success": False
        }