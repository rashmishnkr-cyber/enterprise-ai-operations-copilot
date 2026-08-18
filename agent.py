from dotenv import load_dotenv
from openai import OpenAI

from tools.knowledge_tool import ask_question
from tools.sql_tool import run_sql

load_dotenv()

client = OpenAI()

# -------------------------
# Tool Registry
# -------------------------

TOOLS = {
    "knowledge": ask_question,
    "sql": run_sql,
}


def choose_tool(question):

    prompt = f"""
You are an AI router.

Available tools:

knowledge
- Company policies
- Definitions
- SOPs
- Manuals
- Documentation

sql
- Metrics
- Reports
- Analytics
- Shipment data
- Carrier performance
- Live operational data

Return ONLY ONE WORD:

knowledge

or

sql

Question:

{question}
"""

    response = client.responses.create(
        model="gpt-4.1",
        input=prompt
    )

    return response.output_text.strip().lower()


def agent(question):

    tool = choose_tool(question)

    if tool not in TOOLS:
        tool = "knowledge"

    return TOOLS[tool](question)

