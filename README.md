LangGraph Chatbot
A multi-session conversational AI chatbot built with LangGraph and Streamlit, supporting persistent memory per conversation thread and a clean sidebar-based chat history UI.

Features

Multi-turn conversation with memory via LangGraph's checkpointing system
Multiple independent chat sessions, each identified by a unique thread ID
Sidebar listing all conversations with one-click switching
Real-time streaming responses from the AI backend
Simple "New Chat" button to start a fresh conversation


Project Structure
project/
├── app.py                  # Streamlit frontend (this file)
├── langgraph_backend.py    # LangGraph chatbot definition
└── requirements.txt

Prerequisites

Python 3.10+
A configured langgraph_backend.py that exposes a compiled LangGraph app as chatbot


Installation
bash# 1. Create and activate a virtual environment
python -m venv myenv
myenv\Scripts\activate        # Windows
source myenv/bin/activate     # macOS/Linux

# 2. Install dependencies
pip install streamlit langgraph langchain-core

Running the App
bashstreamlit run app.py
Then open http://localhost:8501 in your browser.

Backend Requirements
Your langgraph_backend.py must export a compiled LangGraph graph named chatbot that:

Accepts {"messages": [HumanMessage(...)]} as input
Is compiled with a checkpointer (e.g., MemorySaver) to support thread_id-based memory
Supports .stream(..., stream_mode="messages") for streaming
Supports .get_state(config=...) to retrieve conversation history

Example minimal backend:
pythonfrom langgraph.graph import StateGraph, MessagesState
from langgraph.checkpoint.memory import MemorySaver
from langchain_groq import ChatGroq

llm = ChatGroq(model="llama-3.3-70b-versatile")

def call_model(state):
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

builder = StateGraph(MessagesState)
builder.add_node("model", call_model)
builder.set_entry_point("model")
builder.set_finish_point("model")

chatbot = builder.compile(checkpointer=MemorySaver())

How It Works
ComponentDescriptionthread_idUUID assigned per chat session, stored in st.session_statechat_threadsList of all thread IDs shown in the sidebarmessage_historyLocal display cache of the active conversationload_conversation()Fetches full message history from LangGraph statereset_chat()Generates a new thread ID and clears the display

Environment Variables
If your backend uses an LLM API, set the appropriate key before running:
bash# For Groq
set GROQ_API_KEY=your_key_here          # Windows
export GROQ_API_KEY=your_key_here       # macOS/Linux

# For OpenAI
set OPENAI_API_KEY=your_key_here

Notes

Conversation history is stored in-memory by default (via MemorySaver). It resets when the server restarts. For persistence across restarts, replace MemorySaver with a database-backed checkpointer (e.g., SqliteSaver or PostgresSaver).
Thread IDs in the sidebar display as full UUIDs. You can modify add_thread() / the sidebar button label to show a custom name or timestamp instead.