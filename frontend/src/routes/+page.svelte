<script lang="ts">
    import { onMount } from 'svelte';
    import type { Student } from '$lib/types';
    import StudentTable from '$lib/components/StudentTable.svelte';
    import StudentDetails from '$lib/components/StudentDetails.svelte';

    let students: Student[] = [];
    let selectedStudent: Student | null = null;
    let loading = true;
    let error: string | null = null;

    onMount(async () => {
        try {
            const response = await fetch('/api/students');
            if (!response.ok) throw new Error('Failed to fetch students');
            students = await response.json();
        } catch (err) {
            error = err instanceof Error ? err.message : 'An error occurred';
        } finally {
            loading = false;
        }
    });

    function handleSelectStudent(student: Student) {
        selectedStudent = student;
    }
</script>

<main>
    <h1>Student Dashboard</h1>

    {#if loading}
        <div class="loading">Loading...</div>
    {:else if error}
        <div class="error">{error}</div>
    {:else}
        <StudentTable 
            {students} 
            onSelectStudent={handleSelectStudent}
        />
        
        {#if selectedStudent}
            <StudentDetails student={selectedStudent} />
        {/if}
    {/if}
</main>

<style>
    main {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }
    .loading, .error {
        text-align: center;
        padding: 20px;
    }
    .error {
        color: red;
    }
</style>