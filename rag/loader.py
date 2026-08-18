import os

from langchain_community.document_loaders import (
    TextLoader,
    PyPDFLoader,
)


def load_documents(data_path="data"):

    documents = []

    for filename in os.listdir(data_path):

        filepath = os.path.join(data_path, filename)

        # Skip folders
        if not os.path.isfile(filepath):
            continue

        try:

            if filename.lower().endswith(".md"):

                loader = TextLoader(filepath)

            elif filename.lower().endswith(".pdf"):

                # Skip empty PDFs
                if os.path.getsize(filepath) == 0:
                    print(f"Skipping empty PDF: {filename}")
                    continue

                loader = PyPDFLoader(filepath)

            else:

                print(f"Skipping unsupported file: {filename}")
                continue

            documents.extend(loader.load())

        except Exception as e:

            print(f"Error loading {filename}: {e}")


    return documents