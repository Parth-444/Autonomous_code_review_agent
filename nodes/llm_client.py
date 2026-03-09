import os

from langchain_google_genai import ChatGoogleGenerativeAI

# Constructed ONCE when this module is first imported.
# Python's import system caches modules, so every file that does
# `from nodes.llm_client import llm` gets the exact same instance.
llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    api_key=os.getenv("GOOGLE_API_KEY"),
)
