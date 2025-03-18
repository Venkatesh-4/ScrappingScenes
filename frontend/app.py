import streamlit as st
import requests
import pandas as pd
import json

st.set_page_config(page_title="Student Records", layout="wide")

def fetch_students():
    try:
        response = requests.get("http://localhost:8000/students")
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error fetching data: {str(e)}")
        return None

def main():
    st.title("Student Records Dashboard")
    
    # Fetch data
    students_data = fetch_students()
    
    if students_data:
        # Convert to DataFrame for easier handling
        students = []
        for student in students_data:
            # Ensure all nested JSON is parsed
            for key, value in student.items():
                if isinstance(value, str):
                    try:
                        student[key] = json.loads(value)
                    except json.JSONDecodeError:
                        pass
            
            # Flatten the basic student info
            student_info = {
                "Register No": student.get("register_no", "N/A"),
                "Name": student.get("name", "N/A"),
                "CGPA": student.get("cgpa", "N/A"),
                "Course": student.get("course", "N/A"),
                "School": student.get("school", "N/A"),
                "Course Duration": student.get("course_duration", "N/A")
            }
            students.append(student_info)
        
        df = pd.DataFrame(students)
        
        # Display basic student information
        st.subheader("Students List")
        st.dataframe(df)
        
        # Detailed view for selected student
        st.subheader("Student Details")
        selected_student = st.selectbox(
            "Select a student to view details",
            options=df["Register No"].tolist(),
            format_func=lambda x: f"{x} - {df[df['Register No']==x]['Name'].iloc[0]}"
        )
        
        if selected_student:
            student = next(s for s in students_data if s["register_no"] == selected_student)
            
            # Create tabs for different views
            tabs = st.tabs(["Overview", "Semesters", "Subjects"])
            
            with tabs[0]:
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Personal Information**")
                    st.write(f"Name: {student.get('name', 'N/A')}")
                    st.write(f"Register No: {student.get('register_no', 'N/A')}")
                    st.write(f"Course: {student.get('course', 'N/A')}")
                with col2:
                    st.write("**Academic Information**")
                    st.write(f"School: {student.get('school', 'N/A')}")
                    st.write(f"CGPA: {student.get('cgpa', 'N/A')}")
                    st.write(f"Course Duration: {student.get('course_duration', 'N/A')}")
            
            with tabs[1]:
                # First, ensure semesters is properly parsed if it's a string
                semesters = student["semesters"]
                if isinstance(semesters, str):
                    semesters = json.loads(semesters)
                
                if semesters:
                    for semester in semesters:
                        with st.expander(f"Semester {semester.get('semester_no', 'N/A')}"):
                            st.write(f"SGPA: {semester.get('sgpa', 'N/A')}")
                            st.write(f"Total Credits: {semester.get('total_credits', 'N/A')}")
                            st.write(f"Earned Credits: {semester.get('earned_credits', 'N/A')}")
                            st.write(f"Result Status: {semester.get('result_status', 'N/A')}")
            
            with tabs[2]:
                semesters = student["semesters"]
                if isinstance(semesters, str):
                    semesters = json.loads(semesters)
                
                if semesters:
                    semester_choice = st.selectbox(
                        "Select Semester",
                        options=[sem.get('semester_no', 'N/A') for sem in semesters]
                    )
                    
                    selected_sem = next((sem for sem in semesters 
                                     if sem.get('semester_no') == semester_choice), None)
                    
                    if selected_sem and selected_sem.get("subjects"):
                        subjects = selected_sem["subjects"]
                        if isinstance(subjects, str):
                            subjects = json.loads(subjects)
                        subjects_df = pd.DataFrame(subjects)
                        st.dataframe(subjects_df)

if __name__ == "__main__":
    main() 