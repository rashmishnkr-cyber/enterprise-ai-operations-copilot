Enterprise AI Operations Copilot 

An enterprise-grade AI assistant that combines Retrieval-Augmented Generation (RAG), SQL Server analytics, and Large Language Models (LLMs) to answer business questions from company documentation and live operational data. 

Features 

Knowledge Assistant (RAG): Answers questions from Markdown and PDF documents using OpenAI Embeddings and ChromaDB. 

SQL Analytics Assistant: Converts natural language into SQL and queries SQL Server. 

AI Agent: Routes requests to the appropriate tool. 

Streamlit Web Application. 

Architecture 

Streamlit UI → AI Agent → LLM Router → Knowledge Tool (ChromaDB) or SQL Tool (SQL Server) → OpenAI GPT-4.1 

Technology Stack 

Python 

OpenAI GPT-4.1 

LangChain 

ChromaDB 

Streamlit 

Microsoft SQL Server 

pyodbc 

Pandas 

PyPDF 

python-dotenv 

Installation 

Clone the repository. 

Create and activate a virtual environment. 

Install dependencies with: pip install -r requirements.txt 

Create a .env file containing OPENAI_API_KEY. 

Build the vector database: python rag/index.py 

Run the application: streamlit run app.py 

Example Questions 

What is OTIF? 

When are cycle counts performed? 

Show shipment count by carrier. 

List carrier metrics. 

Future Enhancements 

OpenAI Function Calling 

LangGraph 

MCP 

Excel Analytics Tool 

Power BI Integration 

Conversation Memory 

Azure Deployment 

Skills Demonstrated 

Retrieval-Augmented Generation (RAG) 

AI Agents 

Prompt Engineering 

Vector Databases 

SQL Server Integration 

Enterprise AI Architecture 

Python 

Streamlit 

Author 

Rashmi Shankar 
LinkedIn: <Rashmi Shankar | LinkedIn > 
GitHub: <rashmishnkr-cyber (Rashmi Shankar) >