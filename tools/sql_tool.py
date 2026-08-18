import pyodbc
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()

# OpenAI Client
client = OpenAI()

# SQL Server Connection
connection = pyodbc.connect(
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=localhost;"
    "DATABASE=Logistics Analytics;"
    "Trusted_Connection=yes;"
)

cursor = connection.cursor()

# Database Schema
SCHEMA = """
Database: Logistics Analytics

View:
vw_carrier_metrics

Columns:
- carrier_id
- shipment_count
"""


def generate_sql(question):

    prompt = f"""
You are an expert SQL Server developer.

Generate ONLY SQL.

Database Schema:

{SCHEMA}

Question:
{question}

Rules:
- SQL Server syntax only.
- Return ONLY SQL.
- No markdown.
- No explanation.
"""

    response = client.responses.create(
        model="gpt-4.1",
        input=prompt
    )

    return response.output_text.strip()


def execute_sql(sql):

    cursor.execute(sql)

    rows = cursor.fetchall()

    return rows


def run_sql(question):

    try:

        sql = generate_sql(question)

        rows = execute_sql(sql)

        if len(rows) == 0:
            return "No records found."

        output = ""

        for row in rows:
            output += str(row) + "\n"

        return f"""
Question:
{question}

------------------------

Generated SQL:

{sql}

------------------------

Results:

{output}
"""

    except Exception as e:

        return f"SQL Error:\n\n{e}"

