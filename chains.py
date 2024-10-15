import os 
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.exceptions import OutputParserException

from dotenv import load_dotenv
load_dotenv()

class Chain:
    def __init__(self):
        self.llm = ChatGroq( model="llama-3.1-70b-versatile", temperature=0,max_tokens=None, timeout=None, max_retries=2,)

    def extract_jobs(self, cleaned_text):
        prompt_extract = PromptTemplate.from_template(
        """
        ### SCRAPED TEXT FROM THE PAGE: {cleaned_text} ##

        The scraped text is from the given url of the job posting.  Extract the job postings and return a JSON file that contains:
        keys: 'role', 'experience', 'skills', and 'descriptions'. 
        Return only valid JSON 
        ### VALID JSON (NO PREAMBLE):
        """
        ) 

        chain_extract = prompt_extract |  self.llm
        data= chain_extract.invoke(input={'cleaned_text':cleaned_text})
        try:
            json_parser=JsonOutputParser()
            data=json_parser.parse(data.content)
        except OutputParserException:
            raise OutputParserException("There is an error while parsing the output")
        return data if isinstance(data, list) else [data]
    def write_mail(self, job, project, links):
        prompt_email = PromptTemplate.from_template(
                """
                ### JOB DESCRIPTION: {job_description}
                ### INSTRUCTION:
                Write as if your name is Piyush kant,You are a data scientist at Stimscience India. You are looking for a great opportunity that is available in the job post.
                your portfoli is available as csv file in which the skill and the project name is given. Links for some of the projects are also available in the same csv file.
                If there is no link associated with the rellevent skill, just mention the skill and project name without mentioning the link. 
                if the skill matches in the job posting, include the skill, and details that matches in the file.
                If the skill is not available in the techstack that I provided then dont mention those skills in the email.
                Your job is to write an email like cover letter to the hiriring team regarding the job mentioned above describing your capability in fulfilling their needs.
                Also add the most relevant skills for that job and the project that is relevent to it in {project}. Also, include the link if and only if the link is mentioned in that row  {link4list}
                Remember you are Piyush, Data Scientist at StimScience. 
                Do not provide a preamble.
                strictly Do not include any skill that is not included in the links 
                ### EMAIL (NO PREAMBLE):
                
                """
                )

        chain_email = prompt_email | self.llm
        res = chain_email.invoke({"job_description": str(job),"project":project, "link4list": links})
        return res.content
if __name__=="__main__":
    print("The stored api key is :{os.getenv('GROQ_API_KEY')}")