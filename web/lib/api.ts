export interface ContextItem {
    id: string;
    text: string;
    source: string;
    type: string;
    timestamp: number;
    score: number;
}

export interface SearchResponse {
    query: string;
    answer: string;
    context: ContextItem[];
}

export async function searchMemory(query: string): Promise<SearchResponse> {
    try {
        const res = await fetch("http://localhost:8000/search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ query, limit: 5 }),
        });

        if (!res.ok) {
            throw new Error(`API Error: ${res.statusText}`);
        }

        return await res.json();
    } catch (error) {
        console.error("Search failed:", error);
        // Return dummy data/error for UI handling
        return {
            query,
            answer: "Error connecting to Neural Shadow Core. Is the backend running?",
            context: [],
        };
    }
}
