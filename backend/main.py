import os

from dotenv import load_dotenv

load_dotenv()

from fastapi import Depends, FastAPI, File, Form, Header, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import AIMessage, HumanMessage
from pydantic import BaseModel

from agent.graph import agent_graph
from rag.documents import delete_document, list_documents, store_uploaded_pdf, store_url_document

app = FastAPI(title="Portfolio Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatMessage(BaseModel):
    role: str  # "user" | "assistant"
    content: str


class ChatRequest(BaseModel):
    message: str
    history: list[ChatMessage] = []


class ChatResponse(BaseModel):
    response: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    messages = [
        HumanMessage(content=m.content) if m.role == "user" else AIMessage(content=m.content)
        for m in request.history
    ]
    result = agent_graph.invoke(
        {
            "messages": messages,
            "query": request.message,
            "intent": "",
            "rag_results": [],
            "response": "",
        }
    )
    return ChatResponse(response=result["response"])


def require_admin(x_admin_key: str = Header(...)) -> None:
    if x_admin_key != os.environ.get("ADMIN_KEY"):
        raise HTTPException(status_code=401, detail="Invalid admin key")


class UrlIngestRequest(BaseModel):
    title: str
    url: str


class DocumentSummary(BaseModel):
    id: str
    title: str
    source_type: str
    created_at: str


@app.get("/kb/documents", response_model=list[DocumentSummary], dependencies=[Depends(require_admin)])
def get_documents():
    return list_documents()


@app.post("/kb/documents/upload", dependencies=[Depends(require_admin)])
def upload_document(title: str = Form(...), file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF uploads are supported")
    chunk_count = store_uploaded_pdf(title, file.filename, file.file.read())
    return {"title": title, "chunks": chunk_count}


@app.post("/kb/documents/url", dependencies=[Depends(require_admin)])
def ingest_url(request: UrlIngestRequest):
    chunk_count = store_url_document(request.title, request.url)
    return {"title": request.title, "chunks": chunk_count}


@app.delete("/kb/documents/{document_id}", dependencies=[Depends(require_admin)])
def remove_document(document_id: str):
    delete_document(document_id)
    return {"deleted": document_id}
