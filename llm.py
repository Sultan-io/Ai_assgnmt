import os 
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
load_dotenv()
GROQ_MODEL="groq:openai/gpt-oss-20b"
API_KEY=os.getenv("GROQ_API_KEY") or os.getenv("API_KEY")
llm=init_chat_model(GROQ_MODEL,api_key=API_KEY)