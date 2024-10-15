#%%
from langchain_groq import ChatGroq
from langchain_groq import ChatGroq

llm = ChatGroq( model="llama-3.1-70b-versatile", temperature=0,
    max_tokens=None, timeout=None, max_retries=2,)

response=llm.invoke("who was the second person to be on the moon?")
print(response.content)

#%%
from langchain_community.document_loaders import WebBaseLoader
curUrl = "https://www.epam.com/careers/job-listings/job.epamgdo_blt1929b43bead763ea_en-us_Hyderabad_India.data-scientist_hyderabad_india"
loader = WebBaseLoader(curUrl)
page_data= loader.load().pop().page_content
print(page_data)
# %%
from langchain_core.prompts import PromptTemplate
prompt_extract = PromptTemplate.from_template(
    """
    ### SCRAPED TEXT FROM THE PAGE: {page_data} ##

    The scraped text is from the given url of the job posting.  Extract the job postings and return a JSON file that contains:
    keys: 'role', 'experience', 'skills', and 'descriptions'. 
    Return only valid JSON 
    ### VALID JSON (NO PREAMBLE):
"""
) 

chain_extract = prompt_extract |  llm
data= chain_extract.invoke(input={'page_data':page_data})
print(data.content)
# %%
from langchain_core.output_parsers import JsonOutputParser

json_parser=JsonOutputParser()
json_out=json_parser.parse(data.content)
print(json_out)
# %%
import pandas as pd 
df=pd.read_csv(r"resource\techstacks.csv")
df.head()
# %%
import uuid
import chromadb

client = chromadb.PersistentClient('vectorstore')
collection = client.get_or_create_collection(name="portfolio")

if not collection.count():
    for _, row in df.iterrows():
        collection.add(documents=row["techstacks"],
                       metadatas={"links": row["Links"]},
                       ids=[str(uuid.uuid4())])
# %%
job = json_out
job['skills']
#%%
links = collection.query(query_texts=job['skills'], n_results=2).get('metadatas', [])
links
#%%
prompt_email = PromptTemplate.from_template(
        """
        ### JOB DESCRIPTION:
        {job_description}
        
        ### INSTRUCTION:
        Write as if your name is Piyush kant,You are a data scientist at Stimscience India. Stimscience is an AI & Software Consulting company dedicated to facilitating
        the seamless integration of business processes through automated tools. 
        Over our experience, we have empowered numerous enterprises with tailored solutions, fostering scalability, 
        process optimization, cost reduction, and heightened overall efficiency. 
        Your job is to write a cold email to the client regarding the job mentioned above describing the capability of Stimscience 
        in fulfilling their needs.
        Also add the most relevant ones from the following links to showcase StimScience's portfolio: {link_list}
        Remember you are Piyush, Data Scientist at StimScience. 
        Do not provide a preamble.
        ### EMAIL (NO PREAMBLE):
        
        """
        )

chain_email = prompt_email | llm
res = chain_email.invoke({"job_description": str(job), "link_list": links})
print(res.content)
# %%
