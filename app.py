"""
PROYECTO 1: Agente de Atención con RAG
========================================
Sin LangChain — usa directamente ChromaDB + google-genai (SDK nuevo) + Streamlit
"""

import os
import tempfile
import streamlit as st
import chromadb
from pypdf import PdfReader
from google import genai
from google.genai import types

# ── CONFIG ─────────────────────────────────────────────────────────────────────
GEMINI_MODEL  = "gemini-2.5-flash"
EMBED_MODEL   = "gemini-embedding-001"
CHUNK_SIZE    = 800
CHUNK_OVERLAP = 100
COLLECTION    = "documentos"

# ── Streamlit Page Config ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="RAG Agent – Asistente de Documentos",
    page_icon="📄",
    layout="wide",
)

st.title("📄 Agente RAG – Asistente de Documentos")
st.caption("Carga un PDF y hazle preguntas. El agente responde citando la fuente.")

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Configuración")
    st.markdown("Consigue tu key gratis en [aistudio.google.com](https://aistudio.google.com)")
    api_key = st.text_input("Google Gemini API Key", type="password")
    uploaded_file = st.file_uploader("Sube tu PDF", type=["pdf"])

    if st.button("🗑️ Limpiar base de datos"):
        st.session_state.clear()
        st.success("Base de datos limpiada.")
        st.rerun()

# ── Helpers ────────────────────────────────────────────────────────────────────

def extract_pages(file_bytes: bytes) -> list:
    """Extrae texto de cada página del PDF."""
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(file_bytes)
        tmp_path = tmp.name

    reader = PdfReader(tmp_path)
    os.unlink(tmp_path)

    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        if text.strip():
            pages.append({"text": text, "page": i + 1})
    return pages


def make_chunks(pages: list) -> list:
    """Divide cada página en chunks con overlap."""
    chunks = []
    for p in pages:
        text  = p["text"]
        start = 0
        while start < len(text):
            chunk_text = text[start:start + CHUNK_SIZE]
            if chunk_text.strip():
                chunks.append({"text": chunk_text, "page": p["page"]})
            start += CHUNK_SIZE - CHUNK_OVERLAP
    return chunks


def embed_texts(client, texts: list) -> list:
    """Genera embeddings para una lista de textos (documentos)."""
    result = client.models.embed_content(
        model=EMBED_MODEL,
        contents=texts,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
    )
    return [e.values for e in result.embeddings]


def embed_query(client, query: str) -> list:
    """Genera embedding para la consulta del usuario."""
    result = client.models.embed_content(
        model=EMBED_MODEL,
        contents=[query],
        config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
    )
    return result.embeddings[0].values


@st.cache_resource(show_spinner="Procesando PDF y generando embeddings…")
def build_vectorstore(file_bytes: bytes, filename: str, api_key: str):
    """Procesa el PDF y llena ChromaDB con embeddings."""
    client = genai.Client(api_key=api_key)

    pages  = extract_pages(file_bytes)
    chunks = make_chunks(pages)
    texts  = [c["text"] for c in chunks]
    pages_nums = [c["page"] for c in chunks]

    st.sidebar.info(f"📦 {len(chunks)} fragmentos de {len(pages)} páginas")

    # Generar embeddings en lotes de 20
    all_embeddings = []
    batch_size = 20
    progress = st.sidebar.progress(0, text="Generando embeddings…")
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        embs  = embed_texts(client, batch)
        all_embeddings.extend(embs)
        progress.progress(min((i + batch_size) / len(texts), 1.0))
    progress.empty()

    # Guardar en ChromaDB en memoria
    chroma  = chromadb.Client()
    try:
        chroma.delete_collection(COLLECTION)
    except Exception:
        pass
    collection = chroma.create_collection(COLLECTION)

    collection.add(
        ids        = [f"chunk_{i}" for i in range(len(chunks))],
        embeddings = all_embeddings,
        documents  = texts,
        metadatas  = [{"page": p} for p in pages_nums],
    )
    return collection, client


def search(collection, client, query: str, k: int = 4) -> list:
    """Busca los k fragmentos más relevantes."""
    query_emb = embed_query(client, query)
    results   = collection.query(
        query_embeddings=[query_emb],
        n_results=k,
    )
    docs  = results["documents"][0]
    metas = results["metadatas"][0]
    return [{"text": d, "page": m["page"]} for d, m in zip(docs, metas)]


def ask_gemini(client, context_chunks: list, question: str) -> str:
    """Envía el contexto recuperado + pregunta a Gemini."""
    context = "\n\n---\n\n".join(
        f"[Página {c['page']}]\n{c['text']}" for c in context_chunks
    )

    prompt = f"""Eres un asistente experto. Responde ÚNICAMENTE usando el siguiente contexto extraído de un documento.

CONTEXTO:
{context}

PREGUNTA: {question}

INSTRUCCIONES:
- Responde en español, de forma clara y concisa.
- Si la respuesta no está en el contexto, di: "No encontré información sobre eso en el documento."
- Al final indica entre paréntesis la(s) página(s) fuente, ej: (Fuente: páginas 3 y 5)

RESPUESTA:"""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
    )
    return response.text


# ── Main UI ────────────────────────────────────────────────────────────────────

if not api_key:
    st.info("👈 Ingresa tu API key de Google Gemini en el panel lateral para comenzar.")
    st.stop()

if not uploaded_file:
    st.info("👈 Sube un archivo PDF para empezar.")
    st.stop()

collection, client = build_vectorstore(uploaded_file.read(), uploaded_file.name, api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if msg.get("sources"):
            with st.expander("📚 Fragmentos fuente"):
                for src in msg["sources"]:
                    st.markdown(f"**Página {src['page']}**")
                    st.text(src["text"][:400] + "…")

if question := st.chat_input("Escribe tu pregunta sobre el documento…"):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Buscando en el documento…"):
            sources = search(collection, client, question)
            answer  = ask_gemini(client, sources, question)

        st.markdown(answer)

        with st.expander("📚 Fragmentos fuente"):
            for src in sources:
                st.markdown(f"**Página {src['page']}**")
                st.text(src["text"][:400] + "…")

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
        "sources": sources,
    })
