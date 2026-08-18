from dotenv import load_dotenv
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from loader import load_documents

# Load environment variables
load_dotenv()

# Load all documents using the loader module
documents = load_documents()

# Split documents into chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=300,
    chunk_overlap=50
)

chunks = text_splitter.split_documents(documents)


# Create embedding model
embeddings = OpenAIEmbeddings()


# Build and save Chroma database
vector_db = Chroma.from_documents(
    documents=chunks,
    embedding=embeddings,
    persist_directory="chroma_db"
)

