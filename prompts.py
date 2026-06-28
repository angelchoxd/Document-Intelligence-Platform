def question_answering_prompt(question, context):
    return f"""
You are an AI assistant for document question answering.

Answer the user's question using only the context below.
If the answer is not in the context, say that the document does not contain that information.
Keep the answer clear and concise.
Do not show your thinking process.

Context:
{context}

Question:
{question}

Final answer:
"""


def summary_prompt(text):
    return f"""
You are an AI assistant that summarizes documents.

Create a clear and professional summary of the document below.
Use bullet points.
Focus on key facts, numbers, recommendations, risks, and important conclusions.
Do not show your thinking process.

Document:
{text}

Summary:
"""


def insights_prompt(text):
    return f"""
You are an AI assistant that extracts insights from documents.

Analyze the document below and return:
- Main topics
- Important numbers or KPIs
- Key risks
- Recommendations
- Important dates if any

Keep the answer structured and concise.
Do not show your thinking process.

Document:
{text}

AI Insights:
"""