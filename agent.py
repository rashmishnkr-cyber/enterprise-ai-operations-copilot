import json

from dotenv import load_dotenv
from openai import OpenAI

from tools.knowledge_tool import ask_question
from tools.sql_tool import run_sql


# Load environment variables
load_dotenv()

# OpenAI client
client = OpenAI()


# --------------------------------------------------
# Tool Definitions
# --------------------------------------------------

TOOLS = [
    {
        "type": "function",
        "name": "knowledge_tool",
        "description": (
            "Search company documents and answer questions using "
            "the enterprise knowledge base. Use this for policies, "
            "definitions, SOPs, manuals, procedures, and documentation."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "The user's question about company documentation."
                }
            },
            "required": ["question"],
            "additionalProperties": False,
        },
    },
    {
        "type": "function",
        "name": "sql_tool",
        "description": (
            "Query the Logistics Analytics SQL Server database. "
            "Use this for shipment metrics, carrier performance, "
            "operational analytics, reports, and numerical business data."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "question": {
                    "type": "string",
                    "description": "The user's business analytics question."
                }
            },
            "required": ["question"],
            "additionalProperties": False,
        },
    },
]


# --------------------------------------------------
# Tool Execution
# --------------------------------------------------

def execute_tool(tool_name, arguments):

    if tool_name == "knowledge_tool":

        question = arguments["question"]

        return ask_question(question)


    if tool_name == "sql_tool":

        question = arguments["question"]

        return run_sql(question)


    return f"Unknown tool: {tool_name}"


# --------------------------------------------------
# AI Agent
# --------------------------------------------------

def agent(question):

    response = client.responses.create(
        model="gpt-4.1",
        instructions="""
You are an enterprise AI operations assistant.

You have access to two tools:

1. knowledge_tool
Use it for:
- Company policies
- SOPs
- Manuals
- Definitions
- Documentation
- Procedures

2. sql_tool
Use it for:
- Shipment metrics
- Carrier performance
- Operational analytics
- Reports
- Numerical business questions
- Live SQL Server data

Choose the appropriate tool based on the user's question.

If the question requires information from company documents,
use knowledge_tool.

If the question requires operational data or calculations
from the SQL database, use sql_tool.

After receiving the tool result, provide a clear answer
to the user.

Do not invent business data.
""",
        tools=TOOLS,
        input=question,
    )


    # --------------------------------------------------
    # Process Tool Calls
    # --------------------------------------------------

    tool_outputs = []

    for item in response.output:

        if item.type == "function_call":

            tool_name = item.name

            arguments = json.loads(item.arguments)

            tool_result = execute_tool(
                tool_name,
                arguments
            )

            tool_outputs.append(
                {
                    "type": "function_call_output",
                    "call_id": item.call_id,
                    "output": str(tool_result),
                }
            )


    # --------------------------------------------------
    # Return Final Answer
    # --------------------------------------------------

    if tool_outputs:

        final_response = client.responses.create(
            model="gpt-4.1",
            instructions="""
You are an enterprise AI operations assistant.

Use the tool results provided to answer the user's question.

Do not invent information.

Give the user a concise, business-friendly answer.
""",
            tools=TOOLS,
            input=[
                {
                    "role": "user",
                    "content": question,
                },
                *response.output,
                *tool_outputs,
            ],
        )

        return final_response.output_text


    return response.output_text


# --------------------------------------------------
# Local Test
# --------------------------------------------------

if __name__ == "__main__":

    question = "Show shipment count by carrier"

    answer = agent(question)

    print(answer)