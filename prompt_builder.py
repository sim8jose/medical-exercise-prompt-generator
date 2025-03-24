import streamlit as st
from main import main  # Importing function from separate module
import os

# Enable full-width layout
st.set_page_config(layout="wide")

# Streamlit UI
st.title("Medical Role-Playing Prompt Generator")

# Create two columns (1:2 ratio)
col1, col2 = st.columns([1, 2])

with col1:
    st.header("📥 Input Section")

    uploaded_pdf = st.file_uploader("Upload PDF File", type=["pdf"])
    uploaded_answer = st.file_uploader("Upload Answer File", type=["pdf"])

    character_name = st.text_input("Character Name:", "Dr. Wong")
    teaching_level = st.selectbox("Teaching Level:", ["Junior", "Intermediate", "Expert"], index=0)

    # Initialize session state for prompt if not set
    if "generated_prompt" not in st.session_state:
        st.session_state.generated_prompt = ""

    generate_button = st.button("🚀 Generate Prompt")

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

with col2:
    st.header("📄 Output Section")

    # Display the stored prompt
    st.text_area("Generated Prompt", st.session_state.generated_prompt, height=500)

    # # Copy button with JavaScript-based clipboard copying
    # if st.session_state.generated_prompt:
    #     copy_button = st.button("📋 Copy to Clipboard")
        
    #     if copy_button:
    #         # JavaScript for clipboard copying
    #         js_code = f"""
    #         <script>
    #         navigator.clipboard.writeText(`{st.session_state.generated_prompt}`);
    #         </script>
    #         """
    #         st.markdown(js_code, unsafe_allow_html=True)
    #         st.success("✅ Copied to clipboard! (Use Ctrl+V to paste)")

    # Display cost details
    if "total_tokens" in st.session_state and "total_cost" in st.session_state:
        st.write(f"**🔢 Total Token Usage:** {st.session_state.total_tokens}")
        st.write(f"**💰 Estimated Cost:** ${st.session_state.total_cost:.8f}")
