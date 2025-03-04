import streamlit as st
from openai import OpenAI  # Using OpenAI LLM API
from dotenv import load_dotenv
import os
from src.agents.base_llm_model import BaseLLMModel

# Load environment variables (API keys)
load_dotenv()

# Initialize LLM model
llm_model = BaseLLMModel()

# Set up the page title
st.title("Testing Chatbot Playground")

# Initialize session state for messages and system prompt
if "messages" not in st.session_state:
    st.session_state.messages = []

if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = "You are a helpful assistant."

# Sidebar for dynamic system prompt input
st.sidebar.title("System Prompt")
system_prompt = st.sidebar.text_area(
    "Enter your system prompt here:", st.session_state.system_prompt
)
if system_prompt != st.session_state.system_prompt:
    st.session_state.system_prompt = system_prompt

# Display the system prompt at the top
st.markdown(f"**System Prompt:** {st.session_state.system_prompt}")

# Function to handle model response generation
def get_model_response(prompt: str, system_prompt: str) -> str:
    # Format the message history to include the system message, user messages, and assistant responses
    messages = [{"role": "system", "content": system_prompt}]
    for message in st.session_state.messages:
        messages.append({"role": message["role"], "content": message["content"]})
    
    # Add the new user message
    messages.append({"role": "user", "content": prompt})
    
    # Generate the assistant's response using the LLM model
    return llm_model.generate_completion_full(messages)

# Display previous chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask me something!"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Generate assistant's response using LLM model
    response = get_model_response(prompt, st.session_state.system_prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response)
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})

    # Display token usage and cost
    st.markdown(f"**Tokens used:** {llm_model.total_usage_tokens}")
    st.markdown(f"**Total cost:** ${llm_model.total_cost:.4f}")

# Reset chat history
if st.button("Reset Chat"):
    st.session_state.messages = []
    # Reset token usage and cost
    llm_model.total_usage_tokens = 0
    llm_model.total_cost = 0