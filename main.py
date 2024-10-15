import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from techStacks import TechStacks
from utils import clean_text


def create_streamlit_app(llm, techStacks, clean_text):
    st.title("Cover Letter Generator")
    url_input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-39130?from=job%20search%20funnel")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            techStacks.load_techStacks()
            jobs = llm.extract_jobs(data)
            for job in jobs:
                skills = job.get('skills', [])
                links = techStacks.query_links(skills)
                email = llm.write_mail(job, project, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    techStacks = TechStacks()
    st.set_page_config(layout="wide", page_title="email Generator", page_icon="📧")
    create_streamlit_app(chain, techStacks, clean_text)