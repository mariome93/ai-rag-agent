 📄 AI RAG Agent — Document Q&A Chatbot

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
![Gemini](https://img.shields.io/badge/Gemini-2.0_Flash-4285F4?style=flat&logo=google&logoColor=white)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_DB-6366F1?style=flat)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-22C55E?style=flat)

> Chatbot inteligente que responde preguntas sobre cualquier PDF usando **Retrieval-Augmented Generation (RAG)**. Cada respuesta cita la página exacta de donde proviene la información — sin alucinaciones.

---

## ✨ Demo

```
Usuario: ¿Cuáles son las políticas de vacaciones?
Agente:  Según el documento, los empleados tienen derecho a 15 días hábiles
         de vacaciones al año... (Fuente: página 12)
```

---

## 🏗️ Cómo funciona

```
PDF subido por el usuario
        │
        ▼
  Extracción de texto por página (PyPDF)
        │
        ▼
  División en chunks de 800 caracteres con overlap de 100
        │
        ▼
  Embeddings con gemini-embedding-001 (Google)
        │
        ▼
  Almacenamiento en ChromaDB (base vectorial en memoria)
        │
        ▼  ← Pregunta del usuario → búsqueda semántica (top 4 chunks)
        │
        ▼
  Gemini 2.0 Flash genera respuesta solo con el contexto recuperado
        │
        ▼
  Streamlit muestra respuesta + páginas fuente
```

---

## 🚀 Instalación paso a paso

### Paso 1 — Clona el repositorio

```bash
git clone https://github.com/mariome93/ai-rag-agent.git
cd ai-rag-agent
```

### Paso 2 — Crea un entorno virtual (recomendado)

**Mac / Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### Paso 3 — Instala las dependencias

```bash
pip install streamlit chromadb google-genai pypdf
```

### Paso 4 — Obtén tu API key de Gemini (gratis)

1. Ve a [aistudio.google.com](https://aistudio.google.com)
2. Inicia sesión con tu cuenta de Google
3. Clic en **"Get API key"** → **"Create API key"**
4. Copia la key (empieza con `AIza...`)

> No necesitas tarjeta de crédito. El plan gratuito incluye 1,500 requests/día.

### Paso 5 — Corre la aplicación

```bash
streamlit run app.py
```

Se abrirá automáticamente en tu navegador en `http://localhost:8501`

### Paso 6 — Úsala

1. Pega tu API key de Gemini en el panel lateral izquierdo
2. Sube cualquier archivo PDF
3. Espera a que procese los embeddings (barra de progreso)
4. Escribe tu pregunta en el chat y presiona Enter

---

## 📦 Dependencias

| Librería | Versión | Uso |
|---|---|---|
| `streamlit` | ≥1.35 | Interfaz web |
| `google-genai` | última | LLM + Embeddings (Gemini) |
| `chromadb` | ≥0.5 | Base de datos vectorial |
| `pypdf` | ≥4.2 | Extracción de texto de PDFs |

> ⚠️ Usa `google-genai` (SDK nuevo), **no** `google-generativeai` (deprecated).

---

## 🔧 Configuración

Puedes ajustar estos parámetros al inicio de `app.py`:

```python
GEMINI_MODEL  = "gemini-2.0-flash"      # Modelo de chat
EMBED_MODEL   = "gemini-embedding-001"  # Modelo de embeddings
CHUNK_SIZE    = 800                     # Tamaño de cada fragmento
CHUNK_OVERLAP = 100                     # Solapamiento entre fragmentos
```

**Modelos de chat disponibles** (según tu cuenta de Google):
- `gemini-2.0-flash` — rápido y gratuito ✅
- `gemini-2.5-flash` — más capaz, también gratuito ✅
- `gemini-2.5-pro` — el más potente

---

## ⚠️ Límites del plan gratuito

| Modelo | Requests/día | Requests/minuto |
|---|---|---|
| gemini-2.0-flash | 1,500 | 15 |
| gemini-2.5-flash | 500 | 10 |

Si ves un error `429 RESOURCE_EXHAUSTED`, espera unos minutos o el día siguiente. El límite se resetea automáticamente.

---

## 🎯 Casos de uso

- **Onboarding empresarial** — asistente sobre manuales de empleados
- **Legal** — Q&A sobre contratos y reglamentos
- **Soporte técnico** — chatbot sobre documentación de producto
- **Educación** — asistente de estudio sobre libros de texto

---

## 🤝 Parte de mi portafolio AI

- 🔗 [ai-content-pipeline](https://github.com/mariome93/ai-content-pipeline) — Pipeline de automatización de contenido
- 🔗 [ai-brand-auditor](https://github.com/mariome93/ai-brand-auditor) — Auditor de contenido por IA

---

*Desarrollado por [@mariome93](https://github.com/mariome93)*
