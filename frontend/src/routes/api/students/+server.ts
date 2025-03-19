import { json } from "@sveltejs/kit";
import type { RequestHandler } from "./$types";

const BACKEND_URL = "http://localhost:8000"; // Your FastAPI server URL

export const GET: RequestHandler = async () => {
  try {
    const response = await fetch(`${BACKEND_URL}/students`);
    if (!response.ok) throw new Error("Failed to fetch students");
    const students = await response.json();
    return json(students);
  } catch (error) {
    return json({ error: "Failed to fetch students" }, { status: 500 });
  }
};
