from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langgraph.graph.message import add_messages

print("Starting script...")

load_dotenv()

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

llm = ChatGroq(model="llama-3.3-70b-versatile")

def chat_node(state: ChatState):
    print("Node running...")
    messages = state['messages']
    response = llm.invoke(messages)
    print("LLM responded")
    return {'messages': [response]}

graph = StateGraph(ChatState)
graph.add_node('chat_node', chat_node)
graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.compile()

def run_cli_chat():
    initial_state = {
        'messages': [HumanMessage(content='what is the capital of pakistan')]
    }

    result = chatbot.invoke(initial_state)

    while True:
        user_message = input("type here:")
        print('user:', user_message)
        if user_message.strip().lower() in ['exit', 'quit', 'bye']:
            break
        response = chatbot.invoke({'messages':[HumanMessage(content=user_message)]})

        print('AI:', response['messages'][-1].content)
if __name__ == "__main_-":
    run_cli_chat()
