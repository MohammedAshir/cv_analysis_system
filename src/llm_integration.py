import cohere
import os
import json
import time
from dotenv import load_dotenv

# Load API Key from .env
load_dotenv()
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

class LLMAnalyzer:
    def __init__(self):
        if not COHERE_API_KEY:
            raise ValueError("Cohere API Key is missing! Set COHERE_API_KEY in .env file.")
        self.client = cohere.Client(COHERE_API_KEY)

    def analyze_cv(self, structured_data):
        """Sends extracted CV data to LLM and gets analysis."""
        prompt = f"""
        You are a CV analysis assistant. Analyze the following CV and return a structured JSON response.

        CV Data:
        {json.dumps(structured_data, indent=4)}

        Provide your response in JSON format like this:
        {{
            "summary": "Brief summary of the candidate",
            "skills": ["Skill 1", "Skill 2", "Skill 3"],
            "python_dev_fit": "Yes/No with explanation",
            "missing_details": ["Missing detail 1", "Missing detail 2"]
        }}
        """

        retries = 0
        while retries < 3:
            try:
                response = self.client.generate(
                    model="command",  # ✅ Use "command" or "command-nightly"
                    prompt=prompt,  # ✅ Include the prompt
                    max_tokens=500,
                    temperature=0.7
                )

                # ✅ Fix: Ensure correct response format
                if response and response.generations:
                    return response.generations[0].text.strip()
                else:
                    return "LLM response was empty or invalid."

            except cohere.error.RateLimitError:
                retries += 1
                wait_time = 2 ** retries  # Exponential backoff
                print(f"Rate limited. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            except Exception as e:
                return f"Error in LLM processing: {e}"

        return "Failed after multiple retries."
