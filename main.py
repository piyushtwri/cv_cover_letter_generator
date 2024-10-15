import streamlit as st
from langchain_community.document_loaders import WebBaseLoader

from chains import Chain
from techStacks import TechStacks
from utils import clean_text


def create_streamlit_app(llm, techstacks, clean_text):
    st.title("Cover Letter Generator")
    url_input = st.text_input("Enter a URL:", value="https://www.epam.com/careers/job-listings/job.epamgdo_blt1929b43bead763ea_en-us_Hyderabad_India.data-scientist_hyderabad_india")
    submit_button = st.button("Submit")

    if submit_button:
        # try:
        loader = WebBaseLoader([url_input])
        with st.spinner("Loading job description..."):
            data = clean_text(loader.load().pop().page_content)
        techstacks.load_techstacks()
        jobs = llm.extract_jobs(data)
        for job in jobs:
            skills = job.get('skills', [])
            projects = techstacks.query_projects(skills)
            links = techstacks.query_links(skills)
            email = llm.write_mail(job, projects, links)
            st.code(email, language='markdown')
        # except Exception as e:
        #     st.error(f"An Error Occurred: {e}")


if __name__ == "__main__":
    chain = Chain()
    techstacks = TechStacks()
    st.set_page_config(layout="wide", page_title="email Generator", page_icon="📧")
    create_streamlit_app(chain, techstacks, clean_text)