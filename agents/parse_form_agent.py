import os

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from main import OPENAI_API_KEY


load_dotenv()

# Parses the form and returns the list of objects
# describing the data to fill in the page
def parse_form_agent():
    llm = ChatOpenAI(
            temperature=0,
            model_name='gpt-4o-mini',
            OPENAI_API_KEY=os.environ["OPENAI_API_KEY"]
    )
    template = """Given the full page source {page_source}. It is a page for job application. It contains a form. I want you to parse it and return a list of json objects which will help identify all input fields required in the form. It will be used to fill the form using selenium. I want three things from you.
        1. Id: which will uniquely identify the tag
        2. Type: the type of id you found that I will pass in selenium
        3. Desc: Description of the data required by that field in my job application
    """

    prompt_template = PromptTemplate(
        template= template, input_variables=['page_source']
    )

    tools_for_agents = []

    return None
