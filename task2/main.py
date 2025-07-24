import io
import streamlit as st
from langchain_ollama.llms import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
import PyPDF2
#from streamlit import exception

st.set_page_config(page_title="name divider", page_icon="👦",layout="centered")
st.title("AI name List divider")
st.markdown("enter the name list to have it divided by gender")


uploaded_file = st.file_uploader("upload ur file")
analyze = st.button("start analyzing")
def extract_text_from_pdf(pdf_file):
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    text=""
    for page in pdf_reader.pages:
        text+=page.extract_text()+"/n"
    return text
def extract_text_from_file(uploaded_file):
    if uploaded_file.type== "application/pdf":
        return extract_text_from_pdf(io.BytesIO(uploaded_file.read()))
    return uploaded_file.read().decode("utf-8")
if analyze and uploaded_file:
    try:
        file_content = extract_text_from_file(uploaded_file)

        if not file_content.strip():
            st.error("no content")
            st.stop()
        st.subheader("📝 File content:")
        st.code(file_content)
        model = OllamaLLM(model="llama3.2")
        template = """
        you are given this text and your task is to divide the names by their gender : male or female and type them into the terminal 
        here is the file: {uploaded_file}
        """
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | model
        with st.spinner("Analyzing names..."):

            result = chain.invoke({"uploaded_file":uploaded_file})
            st.success("✅ Done!")
            st.subheader("👥 Gendered Names:")
            st.write(result)


    except Exception as e:
        st.error(f"an error accured: {str(e)}")