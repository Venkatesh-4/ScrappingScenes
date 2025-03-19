<script lang="ts">
    import type { Student, Semester, Subject } from '$lib/types';
    export let student: Student;
    
    let activeTab = 'overview';
    let selectedSemesterId: string | null = null;
    
    console.log('Student data:', student);
    console.log('Semesters:', student.semesters);
    
    $: sortedSemesters = student ? 
        [...JSON.parse(student.semesters)].sort((a, b) => a.semester_no - b.semester_no) : 
        [];
        
    function viewSemesterDetails(semester) {
        // Set the active tab to semesters
        activeTab = 'semesters';
        // Store the selected semester ID to scroll to it
        selectedSemesterId = `${semester.semester_no}-${semester.exam_schedule_timetable_id}`;
        
        // Use setTimeout to ensure the DOM has updated before scrolling
        setTimeout(() => {
            const element = document.getElementById(`semester-${selectedSemesterId}`);
            if (element) {
                element.scrollIntoView({ behavior: 'smooth' });
            }
        }, 100);
    }
</script>

<style>
    .student-details {
        background-color: #fff;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
        padding: 2rem;
        max-width: 1200px;
        margin: 0 auto;
    }
    
    .header {
        display: flex;
        align-items: center;
        margin-bottom: 2rem;
        border-bottom: 1px solid #eaeaea;
        padding-bottom: 1.5rem;
    }
    
    .avatar {
        width: 80px;
        height: 80px;
        background-color: #6366f1;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-size: 2rem;
        font-weight: bold;
        margin-right: 1.5rem;
    }
    
    .student-info {
        flex: 1;
    }
    
    .student-info h2 {
        margin: 0 0 0.5rem 0;
        color: #1f2937;
        font-size: 1.8rem;
    }
    
    .student-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 1.5rem;
        margin-top: 0.5rem;
    }
    
    .meta-item {
        display: flex;
        align-items: center;
        color: #4b5563;
    }
    
    .meta-item strong {
        margin-right: 0.5rem;
        color: #374151;
    }
    
    .tabs {
        display: flex;
        border-bottom: 1px solid #eaeaea;
        margin-bottom: 2rem;
    }
    
    .tab {
        padding: 0.75rem 1.5rem;
        cursor: pointer;
        color: #6b7280;
        font-weight: 500;
        transition: all 0.2s ease;
        border-bottom: 2px solid transparent;
    }
    
    .tab:hover {
        color: #4f46e5;
    }
    
    .tab.active {
        color: #4f46e5;
        border-bottom: 2px solid #4f46e5;
    }
    
    .tab-content {
        padding: 1rem 0;
    }
    
    .overview-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
        gap: 1.5rem;
        margin-bottom: 2rem;
    }
    
    .stat-card {
        background-color: #f9fafb;
        border-radius: 8px;
        padding: 1.5rem;
        transition: transform 0.2s ease;
    }
    
    .stat-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    .stat-card h3 {
        margin: 0 0 0.5rem 0;
        color: #4b5563;
        font-size: 1rem;
        font-weight: 500;
    }
    
    .stat-card .value {
        font-size: 2rem;
        font-weight: bold;
        color: #1f2937;
    }
    
    .semesters {
        display: grid;
        grid-template-columns: 1fr;
        gap: 2rem;
    }
    
    .overview-semesters {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
        gap: 2rem;
    }
    
    .overview-semesters .semester-card {
        cursor: pointer;
    }
    
    .semester-card {
        background-color: #f9fafb;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .semester-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    
    .highlighted-semester {
        border: 2px solid #4f46e5;
        box-shadow: 0 0 15px rgba(99, 102, 241, 0.4);
    }
    
    .semester-card h4 {
        margin: 0;
        padding: 1rem;
        background-color: #6366f1;
        color: white;
        font-size: 1.2rem;
    }
    
    .semester-details {
        padding: 1.5rem;
    }
    
    .semester-info {
        margin-bottom: 1.5rem;
    }
    
    .semester-info p {
        margin: 0.5rem 0;
        color: #4b5563;
    }
    
    .semester-info strong {
        color: #374151;
    }
    
    .subjects-section h5 {
        margin: 0 0 1rem 0;
        color: #374151;
        font-size: 1.1rem;
        border-bottom: 1px solid #e5e7eb;
        padding-bottom: 0.5rem;
    }
    
    table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.9rem;
    }
    
    th {
        text-align: left;
        padding: 0.75rem 0.5rem;
        border-bottom: 1px solid #e5e7eb;
        color: #6b7280;
        font-weight: 500;
    }
    
    td {
        padding: 0.75rem 0.5rem;
        border-bottom: 1px solid #e5e7eb;
        color: #4b5563;
    }
    
    tr:last-child td {
        border-bottom: none;
    }
    
    small {
        color: #9ca3af;
        font-size: 0.75rem;
    }
    
    .loading {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 200px;
        font-size: 1.2rem;
        color: #6b7280;
    }
    
    @media (max-width: 768px) {
        .header {
            flex-direction: column;
            align-items: flex-start;
        }
        
        .avatar {
            margin-bottom: 1rem;
        }
        
        .semesters {
            grid-template-columns: 1fr;
        }
        
        .overview-grid {
            grid-template-columns: 1fr;
        }
        
        .student-meta {
            flex-direction: column;
            gap: 0.5rem;
        }
    }
</style>

{#if !student}
    <div class="loading">Loading...</div>
{:else}
    <div class="student-details">
        <div class="header">
            <div class="avatar">{student.name.charAt(0)}</div>
            <div class="student-info">
                <h2>{student.name}</h2>
                <div class="student-meta">
                    <div class="meta-item">
                        <strong>Register No:</strong> {student.register_no}
                    </div>
                    <div class="meta-item">
                        <strong>Course:</strong> {student.course}
                    </div>
                    <div class="meta-item">
                        <strong>School:</strong> {student.school}
                    </div>
                    <div class="meta-item">
                        <strong>Duration:</strong> {student.course_duration}
                    </div>
                </div>
            </div>
        </div>
        
        <div class="tabs">
            <div class="tab {activeTab === 'overview' ? 'active' : ''}" on:click={() => activeTab = 'overview'}>
                Overview
            </div>
            <div class="tab {activeTab === 'semesters' ? 'active' : ''}" on:click={() => activeTab = 'semesters'}>
                Semesters
            </div>
        </div>
        
        <div class="tab-content">
            {#if activeTab === 'overview'}
                <div class="overview-grid">
                    <div class="stat-card">
                        <h3>CGPA</h3>
                        <div class="value">{student.cgpa || 'N/A'}</div>
                    </div>
                    <div class="stat-card">
                        <h3>Total Exams Given</h3>
                        <div class="value">{sortedSemesters.length}</div>
                    </div>
                    <div class="stat-card">
                        <h3>Total Exams Cleared</h3>
                        <div class="value">{sortedSemesters.filter(s => s.result_status === 'Successful').length}</div>
                    </div>
                </div>
                
                <div class="overview-semesters">
                    {#if !sortedSemesters || sortedSemesters.length === 0}
                        <p>No semester data available</p>
                    {:else}
                        {#each sortedSemesters as semester (`${semester.semester_no}-${semester.exam_schedule_timetable_id}`)}
                            <div class="semester-card" on:click={() => viewSemesterDetails(semester)}>
                                <h4>Semester {semester.semester_no} ({semester.passing_month} {semester.passing_year})</h4>
                                <div class="semester-details">
                                    <div class="semester-info">
                                        <p><strong>Result:</strong> <span style="color: {semester.result_status === 'Successful' ? '#10b981' : '#ef4444'}">{semester.result_status}</span></p>
                                        <p><strong>SGPA:</strong> {semester.sgpa || 'N/A'}</p>
                                        <p><strong>Credits:</strong> {semester.earned_credits}/{semester.total_credits}</p>
                                        <p><strong>Marks:</strong> {semester.obtained_marks}/{semester.out_of_marks}</p>
                                    </div>
                                </div>
                            </div>
                        {/each}
                    {/if}
                </div>
            {:else if activeTab === 'semesters'}
                <div class="semesters">
                    {#if !sortedSemesters || sortedSemesters.length === 0}
                        <p>No semester data available</p>
                    {:else}
                        {#each sortedSemesters as semester (`${semester.semester_no}-${semester.exam_schedule_timetable_id}`)}
                            <div 
                                id="semester-{semester.semester_no}-{semester.exam_schedule_timetable_id}" 
                                class="semester-card {selectedSemesterId === `${semester.semester_no}-${semester.exam_schedule_timetable_id}` ? 'highlighted-semester' : ''}"
                            >
                                <h4>Semester {semester.semester_no} ({semester.passing_month} {semester.passing_year})</h4>
                                <div class="semester-details">
                                    <div class="semester-info">
                                        <p><strong>Result:</strong> <span style="color: {semester.result_status === 'Successful' ? '#10b981' : '#ef4444'}">{semester.result_status}</span></p>
                                        <p><strong>SGPA:</strong> {semester.sgpa || 'N/A'}</p>
                                        <p><strong>Credits:</strong> {semester.earned_credits}/{semester.total_credits}</p>
                                        <p><strong>Marks:</strong> {semester.obtained_marks}/{semester.out_of_marks}</p>
                                    </div>
                                    
                                    <div class="subjects-section">
                                        <h5>Subjects</h5>
                                        <table>
                                            <thead>
                                                <tr>
                                                    <th>Code</th>
                                                    <th>Subject</th>
                                                    <th>Internal</th>
                                                    <th>External</th>
                                                    <th>Grade</th>
                                                    <th>Credits</th>
                                                </tr>
                                            </thead>
                                            <tbody>
                                                {#each semester.subjects as subject, index (subject.subject_code + '_' + student.register_no + '_' + semester.exam_schedule_timetable_id + '_' + index)}
                                                    <tr style="background-color: {subject.grade.startsWith('F') ? '#fee2e2' : 'transparent'}">
                                                        <td>{subject.subject_code}</td>
                                                        <td>{subject.subject_name}</td>
                                                        <td>
                                                            <span style="color: {subject.internal_marks >= subject.internal_passing_marks ? '#10b981' : '#ef4444'}">
                                                                {subject.internal_marks}/{subject.max_internal_marks}
                                                            </span>
                                                            <br>
                                                            <small>(Pass: {subject.internal_passing_marks})</small>
                                                        </td>
                                                        <td>
                                                            {#if subject.external_marks !== null}
                                                                <span style="color: {subject.external_marks >= subject.external_passing_marks ? '#10b981' : '#ef4444'}">
                                                                    {subject.external_marks}/{subject.max_external_marks}
                                                                </span>
                                                            {:else}
                                                                N/A
                                                            {/if}
                                                            <br>
                                                            <small>(Pass: {subject.external_passing_marks})</small>
                                                        </td>
                                                        <td>
                                                            <span style="font-weight: bold; color: {
                                                                subject.grade === 'O' ? '#10b981' : 
                                                                subject.grade === 'A+' ? '#10b981' : 
                                                                subject.grade === 'A' ? '#10b981' : 
                                                                subject.grade === 'B+' ? '#3b82f6' : 
                                                                subject.grade === 'B' ? '#3b82f6' : 
                                                                subject.grade === 'C' ? '#f59e0b' : 
                                                                subject.grade.startsWith('F') ? '#ef4444' : '#6b7280'
                                                            }">
                                                                {subject.grade}
                                                            </span>
                                                            <br>
                                                            <small>({subject.grade_point})</small>
                                                        </td>
                                                        <td>{subject.credits_obtained}/{subject.max_credits}</td>
                                                    </tr>
                                                {/each}
                                            </tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        {/each}
                    {/if}
                </div>
            {/if}
        </div>
    </div>
{/if}