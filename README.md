# AI Researcher Agent

A full-stack application that automates web research using AI agents, Serper API, and Groq's language models.

## Overview

The AI Researcher Agent helps business professionals and analysts efficiently gather and analyze web information. It demonstrates proficiency in frontend/backend development, API integration, and agentic workflow implementation with LangGraph.

## Key Features

- **Intelligent Search** - Plans and executes web searches based on user queries
- **Information Synthesis** - Analyzes and organizes data into readable format
- **Reflection & Improvement** - Evaluates research quality and refines outputs
- **Real-time Updates** - Provides live progress via WebSockets
- **Chat History** - Stores research queries and results for each user
- **Downloadable Output** - Allows users to download research results

## Architecture

### Backend
- Built with Python and Flask
- Orchestrates AI agents using LangGraph
- Integrates with Serper (search) and Groq (LLMs) APIs
- Uses Flask-SocketIO for real-time communication

### Frontend
- Developed with React and Tailwind CSS
- Provides intuitive interface for research workflow

### Communication
- RESTful APIs for core interactions
- WebSockets for real-time progress updates

## Setup Instructions

### Prerequisites

- Python 3.8+
- Node.js 14+
- npm
- API Keys for [Serper](https://serper.dev) and [Groq](https://groq.com)

### Backend Setup

1. Navigate to backend directory:
   ```bash
   cd backend
   ```

2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file:
   ```
   SERPER_API_KEY=your_serper_api_key
   GROQ_API_KEY=your_groq_api_key
   API_KEY=your_custom_api_key
   ```

### Frontend Setup

1. Navigate to frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create `.env` file:
   ```
   REACT_APP_API_KEY=your_custom_api_key
   REACT_APP_API_URL=http://localhost:5000/api
   REACT_APP_WS_URL=http://localhost:5000
   ```

### Database

The application uses in-memory storage for chat history. For production, consider integrating a persistent database like SQLite or PostgreSQL.

## Running the Application

### Backend

1. Ensure you're in the backend directory with virtual environment activated
2. Start Flask:
   ```bash
   python app.py
   ```
   - Backend runs on http://localhost:5000
   - Check `backend/app.log` for logs and errors

### Frontend

1. Navigate to frontend directory
2. Start React development server:
   ```bash
   npm start
   ```
   - Frontend available at http://localhost:3000

## Usage

1. Open browser to http://localhost:3000
2. Enter research query in the input field
3. Optionally select an LLM model
4. Click "Start Research" to begin
5. Monitor real-time progress updates
6. View structured results upon completion
7. Download results or access past queries from history

## API Documentation

All endpoints except `/api/health` require an `X-Api-Key` header.

| Endpoint | Method | Description | Request Body | Response |
|----------|--------|-------------|-------------|----------|
| `/api/models` | GET | Get available LLM models | N/A | `{"models": ["model1", "model2"], "default": "model1"}` |
| `/api/research` | POST | Start research task | `{"query": "topic", "model": "model_name"}` (model optional) | `{"task_id": "id", "query": "topic", "model": "model_name", "user_id": "id", "status": "started"}` |
| `/api/history` | GET | Get user research history (requires `X-User-ID` header) | N/A | `{"history": [{"id": "query_id", "timestamp": time, "query": "topic", "results": {}}]}` |
| `/api/history` | DELETE | Clear user history (requires `X-User-ID` header) | N/A | `{"success": true}` |
| `/api/health` | GET | Health check | N/A | `{"status": "ok"}` |

## Technologies

### Backend
- Python
- Flask
- LangGraph
- Pydantic
- Flask-SocketIO
- Requests

### Frontend
- React
- Tailwind CSS
- Socket.IO-client

### APIs
- Serper API (web search)
- Groq API (language models)

## Technical Decisions

- **Flask**: Lightweight framework for RESTful APIs
- **React**: Component-based architecture for reusable UI elements
- **WebSockets**: Real-time progress updates for better UX
- **LangGraph**: Flexible orchestration of stateful AI workflows

## Future Improvements

- Integrate persistent database for chat history
- Add user authentication and authorization
- Implement CORS features
- Enhance UI with interactive visualizations
- Support additional data sources beyond web search
- Implement caching for improved performance
- Add multi-language support
