import os
from dotenv import load_dotenv
from openai import OpenAI

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

load_dotenv()

client = OpenAI()

embeddings = OpenAIEmbeddings()

vector_db = Chroma(
    persist_directory="chroma_db",
    embedding_function=embeddings
)

retriever = vector_db.as_retriever(
    search_kwargs={"k": 4}
)
def ask_question(question):

    # Retrieve relevant documents
    results = retriever.invoke(question)

    # Build context for GPT
    context = "\n\n".join(
        doc.page_content for doc in results
    )

    prompt = f"""
You are an enterprise supply chain assistant.

Answer the user's question using ONLY the context below.

If the answer cannot be found in the context,
reply that you could not find the information.

Context:
{context}

Question:
{question}
"""

    response = client.responses.create(
        model="gpt-4.1",
        input=prompt
    )

    # -------------------------
    # Prefer PDF if available
    # -------------------------
    first_doc = None

    for doc in results:
        if "page" in doc.metadata:
            first_doc = doc
            break

    if first_doc is None:
        first_doc = results[0]

    source = os.path.basename(
        first_doc.metadata.get("source", "Unknown")
    )

    page = first_doc.metadata.get("page")

    if page is not None:
        page_text = str(page + 1)
    else:
        page_text = "N/A"

    return f"""
{response.output_text}

--------------------

📄 Source:
{source}

📄 Page:
{page_text}
"""