import { writable } from "svelte/store";
import type { Student } from "$lib/types";

function createStudentStore() {
  const { subscribe, set, update } = writable<{
    students: Student[];
    selectedStudent: Student | null;
    loading: boolean;
    error: string | null;
  }>({
    students: [],
    selectedStudent: null,
    loading: false,
    error: null,
  });

  return {
    subscribe,
    setStudents: (students: Student[]) =>
      update((state) => ({ ...state, students })),
    selectStudent: (student: Student) =>
      update((state) => ({ ...state, selectedStudent: student })),
    setLoading: (loading: boolean) =>
      update((state) => ({ ...state, loading })),
    setError: (error: string | null) =>
      update((state) => ({ ...state, error })),
  };
}

export const studentStore = createStudentStore();
