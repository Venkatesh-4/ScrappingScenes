export interface Student {
  register_no: string;
  name: string;
  cgpa: number | null;
  course: string;
  school: string;
  course_duration: string;
  semesters: string; // Changed from Semester[] to string since it's a JSON string
}

export interface Semester {
  exam_schedule_timetable_id: string;
  semester_no: number;
  result_status: string;
  block_status: boolean;
  block_reason: string | null;
  ordinance: string;
  passing_year: number;
  passing_month: string;
  sgpa: number;
  total_credits: number;
  earned_credits: number;
  obtained_marks: number;
  out_of_marks: number;
  subjects: Subject[];
}

export interface Subject {
  subject_code: string;
  subject_name: string;
  internal_marks: number;
  internal_passing_marks: number;
  max_internal_marks: number;
  external_marks: number;
  external_passing_marks: number;
  max_external_marks: number;
  grade: string;
  grade_point: number;
  credits_obtained: number;
  max_credits: number;
}
