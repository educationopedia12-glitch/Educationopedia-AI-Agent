from langchain_openai import ChatOpenAI

from app.config import OPENROUTER_API_KEY, OPENROUTER_MODEL


llm = ChatOpenAI(
    model=OPENROUTER_MODEL,
    api_key=OPENROUTER_API_KEY,
    base_url="https://openrouter.ai/api/v1",
    temperature=0.7,
)

response = llm.invoke("Hello! Briefly introduce yourself.")

print(response.content)