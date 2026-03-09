from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv(override=True)

# Constructed ONCE when this module is first imported.
# Python's import system caches modules, so every file that does
# `from nodes.llm_client import llm` gets the exact same instance.
llm = ChatGoogleGenerativeAI(model="gemini-3.1-flash-lite-preview", api_key=os.getenv("GEMINI_API_KEY"))
