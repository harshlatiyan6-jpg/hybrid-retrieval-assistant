import streamlit as st
import io

from pypdf import PdfReader

from src.retrieval.qdrant_search import index_pdf
from src.retrieval.rag_engine import (
    retrieve_context,
    generate_answer
)

# ---------------- PAGE CONFIG ----------------

st.set_page_config(
    page_title="HRA | AI Knowledge Workspace",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CUSTOM DESIGN ----------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: #0B1120;
    color: #E8EEF9;
}

[data-testid="stSidebar"] {
    background: #101A2C;
    border-right: 1px solid #24324A;
}

[data-testid="stSidebar"] > div {
    padding-top: 2rem;
}

.block-container {
    max-width: 1350px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

.hero {
    background: linear-gradient(120deg, #162C4B, #173E69);
    border: 1px solid #31547C;
    border-radius: 18px;
    padding: 30px;
    margin-bottom: 24px;
}

.hero-label {
    color: #7FC5FF;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
}

.hero-title {
    color: #FFFFFF;
    font-size: 34px;
    font-weight: 800;
    margin-top: 8px;
}

.hero-subtitle {
    color: #C3D4EA;
    font-size: 15px;
}

.section-title {
    color: #F0F5FF;
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 12px;
}

.metric-card {
    background: #131F33;
    border: 1px solid #263751;
    padding: 20px;
    border-radius: 14px;
    min-height: 110px;
}

.metric-label {
    color: #93A6C2;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.metric-value {
    color: #FFFFFF;
    font-size: 23px;
    font-weight: 800;
    margin-top: 10px;
}

.panel {
    background: #131F33;
    border: 1px solid #263751;
    border-radius: 16px;
    padding: 22px;
    margin-bottom: 18px;
}

.stButton button {
    background: #3478F6;
    color: white;
    border: 1px solid #4B8AFF;
    border-radius: 9px;
    min-height: 44px;
    font-weight: 700;
}

.stButton button:hover {
    background: #2463D6;
    border-color: #6EA2FF;
    color: white;
}

.stTextInput input {
    background: #0E192B;
    color: white;
    border: 1px solid #344660;
    border-radius: 9px;
}

[data-testid="stFileUploader"] {
    background: #0E192B;
    border: 1px dashed #456080;
    border-radius: 12px;
    padding: 14px;
}

[data-testid="stMetric"] {
    background: #131F33;
    border: 1px solid #263751;
    padding: 15px;
    border-radius: 12px;
}

[data-testid="stExpander"] {
    background: #131F33;
    border: 1px solid #263751;
    border-radius: 10px;
}

hr {
    border-color: #263751;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# ---------------- SESSION STATE ----------------

if "indexed_signature" not in st.session_state:
    st.session_state.indexed_signature = None

if "answer" not in st.session_state:
    st.session_state.answer = None

if "sources" not in st.session_state:
    st.session_state.sources = []


# ---------------- SIDEBAR ----------------

with st.sidebar:

    st.markdown("## ✦ HRA")
    st.caption("HYBRID RETRIEVAL ASSISTANT")

    st.divider()

    st.markdown("### WORKSPACE")
    st.markdown("📄  Document Intelligence")
    st.markdown("🔎  Smart Retrieval")
    st.markdown("💬  AI Assistant")

    st.divider()

    st.markdown("### TECHNOLOGY")
    st.caption("Python · Streamlit")
    st.caption("Qdrant · OpenAI")

    st.divider()

    st.markdown("### SYSTEM STATUS")
    st.success("Application running")

    st.caption("Version 1.0.0")


# ---------------- HEADER ----------------

st.markdown("""
<div class="hero">
    <div class="hero-label">AI-POWERED KNOWLEDGE WORKSPACE</div>
    <div class="hero-title">Your Documents. Smarter Answers.</div>
    <p class="hero-subtitle">
        Upload documents, retrieve relevant information
        and explore your knowledge with AI.
    </p>
</div>
""", unsafe_allow_html=True)


# ---------------- METRICS ----------------

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Platform</div>
        <div class="metric-value">AI Workspace</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Vector Database</div>
        <div class="metric-value">Qdrant</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-label">Language Model</div>
        <div class="metric-value">OpenAI</div>
    </div>
    """, unsafe_allow_html=True)


st.write("")
st.divider()


# ---------------- DOCUMENT UPLOAD ----------------

st.markdown(
    '<div class="section-title">01 · Document Intelligence</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="panel">
    <b>Upload your knowledge source</b>
    <p style="color:#93A6C2">
        Add a PDF document to extract, process and index its content.
    </p>
</div>
""", unsafe_allow_html=True)

uploaded_file = st.file_uploader(
    "Choose a PDF document",
    type=["pdf"]
)

pages = []
signature = None

if uploaded_file is not None:

    signature = (
        uploaded_file.name,
        uploaded_file.size
    )

    try:
        reader = PdfReader(
            io.BytesIO(uploaded_file.getvalue())
        )

        for number, page in enumerate(reader.pages, start=1):

            text = page.extract_text() or ""

            if text.strip():
                pages.append({
                    "page": number,
                    "text": text
                })

        left, right = st.columns(2)

        with left:
            st.metric("Total PDF pages", len(reader.pages))

        with right:
            st.metric("Readable pages", len(pages))

        st.caption(f"Selected document: {uploaded_file.name}")

        if st.button(
            "⚡ Process & Index Document",
            use_container_width=True
        ):

            with st.spinner("Processing and indexing document..."):

                count = index_pdf(
                    pages,
                    uploaded_file.name
                )

            st.session_state.indexed_signature = signature
            st.session_state.answer = None
            st.session_state.sources = []

            st.success(
                f"Document indexed successfully · {count} chunks"
            )

    except Exception as e:
        st.error(f"Document processing failed: {e}")


# ---------------- AI QUESTION ANSWERING ----------------

st.divider()

st.markdown(
    '<div class="section-title">02 · AI Knowledge Assistant</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div class="panel">
    <b>Ask questions about your document</b>
    <p style="color:#93A6C2">
        Search relevant document content and generate
        context-grounded answers.
    </p>
</div>
""", unsafe_allow_html=True)


is_indexed = (
    signature is not None
    and signature == st.session_state.indexed_signature
)

if is_indexed:

    question = st.text_input(
        "Your question",
        placeholder="Ask something about your uploaded PDF..."
    )

    if st.button(
        "✦ Generate AI Answer",
        use_container_width=True
    ):

        if not question.strip():

            st.warning("Please enter a question.")

        else:

            try:

                with st.spinner(
                    "Retrieving context and generating answer..."
                ):

                    contexts = retrieve_context(question)

                    if contexts:

                        answer = generate_answer(
                            question,
                            contexts
                        )

                        st.session_state.answer = answer
                        st.session_state.sources = contexts

                    else:

                        st.session_state.answer = (
                            "No relevant information was found."
                        )

                        st.session_state.sources = []

            except Exception as e:

                error_text = str(e)

                if "429" in error_text or "credits" in error_text.lower():

                    st.error(
                        "OpenAI API credits unavailable. "
                        "Please check your API billing."
                    )

                else:

                    st.error(f"AI generation failed: {error_text}")


elif uploaded_file is None:

    st.info("Upload a PDF document to begin.")

else:

    st.warning(
        "Please process and index this document before asking questions."
    )


# ---------------- ANSWER DISPLAY ----------------

if st.session_state.answer:

    st.divider()

    st.markdown("### ✦ AI Generated Response")

    with st.container(border=True):

        st.markdown(st.session_state.answer)

    if st.session_state.sources:

        st.markdown("### 📚 Retrieved Sources")

        for item in st.session_state.sources:

            with st.expander(
                f"Page {item['page']} · Score {item['score']:.3f}"
            ):

                st.write(item["text"])


# ---------------- FOOTER ----------------

st.divider()

st.caption(
    "HYBRID RETRIEVAL ASSISTANT  ·  "
    "Built with Python, Streamlit, Qdrant & OpenAI"
)