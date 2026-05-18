import os
import time
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()

groq_llm = LLM(
    model="groq/llama-3.3-70b-versatile",  # Higher TPM limit (12k vs 6k)
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7,
    max_retries=10,       # Auto retry on rate limit
    timeout=180           # Wait up to 3 mins
)