<script lang="ts">
    import type { Student } from '$lib/types';
    export let students: Student[];
    export let onSelectStudent: (student: Student) => void;
</script>

<table>
    <thead>
        <tr>
            <th>Register No</th>
            <th>Name</th>
            <th>CGPA</th>
            <th>Course</th>
            <th>School</th>
        </tr>
    </thead>
    <tbody>
        {#each students as student}
            <tr on:click={() => onSelectStudent(student)}>
                <td>{student.register_no}</td>
                <td>{student.name}</td>
                <td>{student.cgpa}</td>
                <td>{student.course}</td>
                <td>{student.school}</td>
            </tr>
        {/each}
    </tbody>
</table>

<style>
    table {
        width: 100%;
        border-collapse: collapse;
    }
    th, td {
        padding: 8px;
        border: 1px solid #ddd;
        text-align: left;
    }
    tr:hover {
        background-color: #f5f5f5;
        cursor: pointer;
    }
</style>