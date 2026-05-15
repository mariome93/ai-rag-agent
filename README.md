# 🤖 Portfolio AI Engineering — 3 Proyectos

Proyectos diseñados para demostrar habilidades en **Prompt Engineering**, **LLMs** y **automatización con IA**.

---

## Proyecto 1: Agente RAG 📄
**Carpeta:** `proyecto1_rag/`

Chatbot que responde preguntas sobre cualquier PDF usando Retrieval-Augmented Generation.

**Stack:** Python · LangChain · Anthropic Claude · ChromaDB · Streamlit

```bash
cd proyecto1_rag
pip install -r requirements.txt
# Agrega tu API key de Anthropic
streamlit run app.py
```

**Lo que demuestra:**
- Manejo de documentos privados con LLMs (sin filtrar datos al modelo innecesariamente)
- Arquitectura RAG: chunking → embeddings → vector search → respuesta citada
- UI interactiva lista para demo en vivo

---

## Proyecto 2: Pipeline de Automatización 🔄
**Carpeta:** `proyecto2_pipeline/`

Convierte cualquier texto largo en 3 piezas de contenido lisas para publicar, retornando JSON estructurado integrable con Make.com o n8n.

**Stack:** Python · Anthropic Claude API

```bash
cd proyecto2_pipeline
pip install -r requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."

# Con archivo de texto
python pipeline.py --input ejemplo_input.txt --save

# Con texto directo
python pipeline.py --text "Tu artículo aquí..." --save
```

**Output JSON incluye:**
- `slack_summary` — resumen con bullets y nivel de urgencia
- `linkedin_post` — hook + cuerpo + hashtags + estimación de alcance
- `sentiment_analysis` — score, emociones, tono, recomendaciones

**Lo que demuestra:**
- System prompts avanzados para roles específicos
- Structured outputs (JSON estricto) para integración con otros sistemas
- Manejo de errores y limpieza de respuestas del modelo

---

## Proyecto 3: Auditor de Contenido 🎯
**Carpeta:** `proyecto3_auditor/`

Evalúa qué tan alineado está un texto con las directrices de marca de una empresa, devolviendo una puntuación 0-100 con violaciones concretas y sugerencias de mejora.

**Stack:** Python · Anthropic Claude API

```bash
cd proyecto3_auditor
pip install -r requirements.txt
export ANTHROPIC_API_KEY="sk-ant-..."

# Con brand guidelines personalizados
python auditor.py --input mi_articulo.txt --brand brand_template.json

# Con brand guidelines por defecto (AcmeCorp de ejemplo)
python auditor.py --text "Nuestro producto es literalmente el mejor del mercado..."
```

**Output incluye:**
- Puntuación global y por categoría (tono, reglas, palabras prohibidas, fit de audiencia)
- Lista de violaciones con severidad, cita exacta y sugerencia de reescritura
- Reescritura sugerida del primer párrafo

**Lo que demuestra:**
- Prompt engineering para evaluación estructurada y consistente
- JSON schema enforcement en respuestas del modelo
- Aplicación directa a metodologías de consultoría (ej: auditorías de marca)

---

## Estructura del Repositorio

```
portfolio/
├── README.md                         ← Este archivo
├── proyecto1_rag/
│   ├── app.py                        ← App Streamlit principal
│   └── requirements.txt
├── proyecto2_pipeline/
│   ├── pipeline.py                   ← Script principal
│   ├── ejemplo_input.txt             ← Texto de prueba
│   └── requirements.txt
└── proyecto3_auditor/
    ├── auditor.py                    ← Script principal
    ├── brand_template.json           ← Plantilla de directrices de marca
    └── requirements.txt
```

---

## Habilidades demostradas

| Habilidad | Proyectos |
|---|---|
| Prompt Engineering (System Prompts, roles) | 1, 2, 3 |
| Structured Outputs / JSON enforcement | 2, 3 |
| RAG Architecture | 1 |
| Vector Databases (ChromaDB) | 1 |
| LangChain | 1 |
| Anthropic Claude API | 1, 2, 3 |
| Streamlit (UI) | 1 |
| Automatización / integración con Make.com, n8n | 2 |
| Evaluación y auditoría de contenido con IA | 3 |

---

*Desarrollado como portafolio profesional de AI Engineering / Prompt Engineering.*
