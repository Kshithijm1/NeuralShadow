import requests
import json
from ..config import OLLAMA_URL, LLM_MODEL
from ..utils import log

class LLMClient:
    def __init__(self):
        self.url = OLLAMA_URL
        self.model = LLM_MODEL

    def generate_answer(self, query: str, context: list) -> str:
        """
        Generates an answer using the local LLM based on context.
        """
        if not context:
            prompt = f"User Question: {query}\n\nI have no memory of this. Politely say you couldn't find anything."
        else:
            # Construct Context String
            context_str = "\n\n".join([f"[Source: {c['source']}]: {c['text']}" for c in context])
            
            prompt = f"""You are Neural Shadow, a personal intelligence system. 
You have access to the user's past screen recordings and audio transcripts (Context).
Answer the user's question based strictly on the context provided below.
If the answer is not in the context, say you don't know.

=== CONTEXT ===
{context_str}
=== END CONTEXT ===

User Question: {query}
Answer:"""

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        try:
            log.info(f"Sending prompt to Ollama ({self.model})...")
            response = requests.post(self.url, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data.get("response", "No response from LLM.")
            
        except requests.exceptions.ConnectionError:
            log.error("Could not connect to Ollama. Is it running?")
            return "Error: Could not connect to local LLM (Ollama). Please ensure 'ollama serve' is running."
        except Exception as e:
            log.error(f"LLM Generation Error: {e}")
            return f"Error responding to query: {e}"
