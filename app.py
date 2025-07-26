import streamlit as st
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()
api_key = os.getenv("GROQ_API_KEY")

# Initialize OpenAI client with GROQ
client = OpenAI(
    api_key=api_key,
    base_url="https://api.groq.com/openai/v1"  #GROQ-compatible OpenAI API
)

st.set_page_config(page_title="GROQ Writer", layout="centered")

st.title("✍️ GROQ Writer with Streamlit")
st.write("Generate **Blogs**, **Stories**, or **Code** using GROQ LLM.")

# Sidebar controls
st.sidebar.title("Options")
content_type = st.sidebar.selectbox("Select Content Type", ["Blog", "Story", "Code"])
language = st.sidebar.text_input("Preferred Language (for Code)", value="Python" if content_type == "Code" else "")
temperature = st.sidebar.slider("Creativity (Temperature)", 0.0, 1.0, 0.7)

# User input
prompt = st.text_area("Enter your idea or topic:", height=150)

if st.button("Generate"):
    if not prompt:
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Generating content..."):
            system_message = {
                "Blog": "You are a professional blog writer. Generate an SEO-friendly, informative blog post.",
                "Story": "You are a creative fiction writer. Write an engaging short story.",
                "Code": f"You are a helpful coding assistant. Generate functional code in {language}."
            }

            try:
                response = client.chat.completions.create(
                    model="llama3-70b-8192",  # or another Groq-supported model
                    messages=[
                        {"role": "system", "content": system_message[content_type]},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=temperature,
                    max_tokens=1024,
                    stream=False
                )

                result = response.choices[0].message.content
                st.subheader(f"Generated {content_type}:")
                st.code(result) if content_type == "Code" else st.write(result)

            except Exception as e:
                st.error(f"")
