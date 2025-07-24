import io
import streamlit as st
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import PyPDF2

st.set_page_config(page_title="Name Divider", page_icon="👦", layout="centered")
st.title("AI Name List Divider")
st.markdown("Upload a file with names to divide them by gender.")

uploaded_file = st.file_uploader("📄 Upload your file (.txt or .pdf)", type=["txt", "pdf"])
analyze = st.button("🚀 Start Analyzing")

def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text() + "\n"
    return text

def extract_text_from_file(uploaded_file):
    if uploaded_file.type == "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")

if analyze and uploaded_file:
    try:
        file_content = extract_text_from_file(uploaded_file)

        if not file_content.strip():
            st.error("❌ No content found in the file.")
            st.stop()

        st.subheader("📝 File content:")
        st.code(file_content)

        model = OllamaLLM(model="llama3.2")
        template =template = """
You are an AI assistant. Your task is to take the following list of first names and divide them clearly into two categories: 'Male' and 'Female'.

List of names:
{uploaded_file}

Return ONLY the categorized names like this:

Male:
- name1
- name2

Female:
- name3
- name4

Do not return any code or explanation.
"""

        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | model

        with st.spinner("Analyzing names..."):
            result = chain.invoke({"uploaded_file": file_content})
            st.success("✅ Done!")
            st.subheader("👥 Gendered Names:")
            st.write(result)

    except Exception as e:
        st.error(f"❌ An error occurred: {str(e)}")
