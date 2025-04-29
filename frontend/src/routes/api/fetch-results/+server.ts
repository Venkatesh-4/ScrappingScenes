import { json } from "@sveltejs/kit";
import type { RequestHandler } from "./$types";

const BACKEND_URL = "http://localhost:8000";

export const POST: RequestHandler = async () => {
    try {
        const response = await fetch(`${BACKEND_URL}/api/run-fetcher`, {
            method: 'POST'
        });
        
        if (!response.ok) {
            throw new Error("Failed to run fetcher script");
        }

        const data = await response.json();
        return json(data);
    } catch (error) {
        return json({ 
            success: false,
            output: "",
            error: "Failed to execute fetcher script" 
        }, { status: 500 });
    }
};
