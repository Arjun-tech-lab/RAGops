import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

from dotenv import load_dotenv

from groq import Groq

from retrieval_engine import search_project


# =====================================================
# LOAD ENV
# =====================================================

load_dotenv()


# =====================================================
# FASTAPI APP
# =====================================================

app = FastAPI()


# =====================================================
# CORS
# =====================================================

app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)


# =====================================================
# GROQ CLIENT
# =====================================================

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


# =====================================================
# REQUEST MODEL
# =====================================================

class QueryRequest(BaseModel):

    question: str


# =====================================================
# HEALTH CHECK
# =====================================================

@app.get("/")

def health():

    return {
        "status": "running"
    }


# =====================================================
# MAIN AI ENDPOINT
# =====================================================

@app.post("/ask")

def ask_question(data: QueryRequest):

    # ---------------------------------------------
    # RETRIEVE
    # ---------------------------------------------

    results = search_project(data.question)


    # ---------------------------------------------
    # BUILD CONTEXT
    # ---------------------------------------------

    context = ""


    for result in results[:3]:

        context += f"""

FILE:
{result['metadata']['path']}

TYPE:
{result['metadata']['type']}

CODE:
{result['document']}

"""


    # ---------------------------------------------
    # PROMPT
    # ---------------------------------------------

    prompt = f"""

You are a senior software engineer.

QUESTION:
{data.question}

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
    # GENERATE
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

            result["metadata"]["path"]

            for result in results[:3]
        ]
    }