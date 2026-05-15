import os

from groq import Groq

from retrieval_engine import search_project


# =====================================================
# GROQ CLIENT
# =====================================================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# =====================================================
# GENERATE ANSWER
# =====================================================

def generate_answer(query):

    # ---------------------------------------------
    # RETRIEVE RELEVANT DOCUMENTS
    # ---------------------------------------------

    results = search_project(query)


    # ---------------------------------------------
    # BUILD CONTEXT
    # ---------------------------------------------

    context = ""


    for result in results[:3]:

        metadata = result.get("metadata", {})

        path = metadata.get("path", "unknown")

        file_type = metadata.get("type", "unknown")

        document = result.get("document", "")


        context += f"""

FILE:
{path}

TYPE:
{file_type}

CODE:
{document}

"""


    # ---------------------------------------------
    # PROMPT
    # ---------------------------------------------

    prompt = f"""

You are a senior software engineer.

QUESTION:
{query}

CONTEXT:
{context}

Instructions:

- Answer ONLY using provided context
- Do NOT hallucinate
- Explain architecture clearly
- Mention relevant files
- Keep answers concise but technical

"""


    # ---------------------------------------------
    # GENERATE RESPONSE
    # ---------------------------------------------

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[

            {
                "role": "user",
                "content": prompt
            }

        ]
    )


    answer = response.choices[0].message.content


    # ---------------------------------------------
    # RETURN
    # ---------------------------------------------

    return {

        "answer": answer,

        "sources": [

            result.get(
                "metadata",
                {}
            ).get(
                "path",
                "unknown"
            )

            for result in results[:3]
        ]
    }