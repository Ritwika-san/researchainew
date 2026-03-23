# ResearchAI

An AI-powered research assistant built with Django and Llama 3.1.

## What it does

- Enter any topic and get a structured research summary instantly
- AI remembers your past research, connects and provides related topics (RAG)
- Personal research history saved per user
- Secure authentication system

## Tech Stack

**Backend**
- Django + Django REST Framework
- SQLite database
- ChromaDB vector database

**AI**
- Llama 3.1 via Groq API
- RAG (Retrieval Augmented Generation)
- Sentence Transformers for embeddings

**Frontend**
- HTML, CSS, Bootstrap 5
- Vanilla JavaScript (fetch API)

## Architecture
```
User submits topic
→ Django checks ChromaDB for similar past research (RAG)
→ Sends topic + context to Llama 3.1 via Groq
→ AI generates structured research summary
→ Result saved to SQLite + ChromaDB
→ Displayed to user instantly
```

## Setup

1. Clone the repo
2. Create virtual environment
```
   python -m venv venv
   venv\Scripts\activate
```
3. Install dependencies
```
   pip install -r requirements.txt
```
4. Create `.env` file
```
   SECRET_KEY=your_django_secret_key
   DEBUG=True
   GROQ_API_KEY=your_groq_api_key
```
5. Run migrations
```
   python manage.py migrate
```
6. Start server
```
   python manage.py runserver
```

## Key Concepts Implemented

- Custom Django User model with email authentication
- REST API endpoints with DRF
- RAG pipeline using ChromaDB + Sentence Transformers
- Agentic AI with context-aware responses
- Secure API key management with python-dotenv