import streamlit as st
from main import main  # Importing function from separate module
import os
from dotenv import load_dotenv
from src.agents.base_llm_model import BaseLLMModel

# Load environment variables
load_dotenv()

# Initialize LLM model
llm_model = BaseLLMModel()

# Enable full-width layout
st.set_page_config(layout="wide")

# Streamlit UI
st.title("Medical Role-Playing Prompt Tester")

# Display total tokens & cost below the title
if "total_tokens" not in st.session_state:
    st.session_state.total_tokens = 0
if "total_cost" not in st.session_state:
    st.session_state.total_cost = 0

st.markdown(f"**🔢 Total Tokens Used:** {st.session_state.total_tokens}")
st.markdown(f"**💰 Total Cost Spent:** ${st.session_state.total_cost:.8f}")

# Create two tabs
tab1, tab2 = st.tabs(["📝 Prompt Builder", "🤖 Prompt Tester"])

with tab1:
    st.header("📥 Prompt Generator")

    col1, col2 = st.columns([1, 2])  # Input on left, output on right

    with col1:
        uploaded_pdf = st.file_uploader("Upload PDF File", type=["pdf"])
        uploaded_answer = st.file_uploader("Upload Answer File", type=["pdf"])

        character_name = st.text_input("Character Name:", "Dr. Wong")
        teaching_level = st.selectbox("Teaching Level:", ["Junior", "Intermediate", "Expert"], index=0)

        # Initialize session state for prompt
        if "generated_prompt" not in st.session_state:
            st.session_state.generated_prompt = ""
        
        generate_button = st.button("🚀 Generate Prompt")

    with col2:
        st.subheader("Generated Prompt")
        
        if generate_button:
            if uploaded_pdf and uploaded_answer:
                os.makedirs("temp", exist_ok=True)
                pdf_path = os.path.join("temp", uploaded_pdf.name)
                answer_path = os.path.join("temp", uploaded_answer.name)

                with open(pdf_path, "wb") as f:
                    f.write(uploaded_pdf.getbuffer())

                with open(answer_path, "wb") as f:
                    f.write(uploaded_answer.getbuffer())

                with st.spinner("⏳ Generating..."):
                    prompt, total_tokens, total_cost = main(
                        pdf_path=pdf_path, 
                        answer_path=answer_path, 
                        output_path=None, 
                        character_name=character_name, 
                        teaching_level=teaching_level,
                    )
                
                # Save to session state
                st.session_state.generated_prompt = prompt
                st.session_state.total_tokens = total_tokens
                st.session_state.total_cost = total_cost
                
                st.success("✅ Prompt Generated Successfully!")

        st.text_area("Generated Prompt", st.session_state.generated_prompt, height=250)
        
        if "total_tokens" in st.session_state and "total_cost" in st.session_state:
            st.write(f"**🔢 Total Token Usage:** {st.session_state.total_tokens}")
            st.write(f"**💰 Estimated Cost:** ${st.session_state.total_cost:.8f}")

with tab2:
    st.header("🤖 Test the Generated Prompt")
    
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Custom Prompt Input")
        
        if "custom_prompt" not in st.session_state:
            st.session_state.custom_prompt = st.session_state.get("generated_prompt", "")

        custom_prompt = st.text_area("Enter a custom prompt:", st.session_state.custom_prompt)
        
        begin_test_button = st.button("🚀 Begin Testing")

        if begin_test_button and custom_prompt.strip():
            st.session_state.start_chat = True  # Enable chat interface
            st.session_state.chat_history = [
                {"role": "system", "content": custom_prompt}
            ]

            # Chatbot sends first message based on system prompt
            with st.spinner("🤖 Generating initial response..."):
                first_response = llm_model.generate_completion_full([
                    {"role": "system", "content": custom_prompt}
                ])
                st.session_state.chat_history.append({"role": "assistant", "content": first_response})

                # Update token usage and cost
                st.session_state.total_tokens += llm_model.total_usage_tokens
                st.session_state.total_cost += llm_model.total_cost

            st.success("✅ Chatbot initialized! Start chatting.")

    with col2:
        st.subheader("Chatbot Interface")

        if st.session_state.get("start_chat", False):
            chat_container = st.container()

            # Display chat messages
            with chat_container:
                for message in st.session_state.chat_history:
                    with st.chat_message(message["role"]):
                        st.markdown(message["content"])

            user_input = st.chat_input("Ask the chatbot!")  # Ensures input stays at the bottom

            if user_input:
                st.session_state.chat_history.append({"role": "user", "content": user_input})

                with st.spinner("🤖 Generating response..."):
                    bot_response = llm_model.generate_completion_full(st.session_state.chat_history)

                st.session_state.chat_history.append({"role": "assistant", "content": bot_response})

                # Update token usage and cost
                st.session_state.total_tokens += llm_model.total_usage_tokens
                st.session_state.total_cost += llm_model.total_cost

                # Re-render chat messages
                with chat_container:
                    with st.chat_message("user"):
                        st.markdown(user_input)
                    with st.chat_message("assistant"):
                        st.markdown(bot_response)

# Reset all session states
if st.button("🔄 Reset All"):
    st.session_state.generated_prompt = ""
    st.session_state.chatbot_response = ""
    st.session_state.chat_history = []
    st.session_state.start_chat = False
    st.session_state.total_tokens = 0
    st.session_state.total_cost = 0
