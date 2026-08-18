import pandas as pd


def load_excel(file_path):

    df = pd.read_excel(file_path)

    return df


def run_excel(file_path, question):

    df = load_excel(file_path)

    return f"""
Question:
{question}

Rows: {len(df)}

Columns:

{list(df.columns)}

Preview:

{df.head()}
"""


if __name__ == "__main__":

    result = run_excel(
        "sample.xlsx",
        "Summarize this file"
    )

    print(result)