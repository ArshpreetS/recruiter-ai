import schedule
import time
from tools.utils import get_telegram_messages
import os
from langchain_openai import ChatOpenAI
from langchain.agents import (
        AgentExecutor,
        create_react_agent
)
from langchain import hub
from langchain_core.prompts import PromptTemplate


LAST_UPDATE_ID_RECEIVED = 0
OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]

def is_job_application_message(message):
    llm = ChatOpenAI(
     api_key=OPENAI_API_KEY, 
     temperature=0,
     model="gpt-4o-mini")

    template = """given this telegram message content: {message_content} I want you to tell me if this message contains any link for job application. If it is then Your answer should contain only the URL to application, else just say "No" """

    prompt_template = PromptTemplate(
        template=template, input_variables=["message_content"]
    )

    #tools_for_agent = []
    #react_prompt = hub.pull("hwchase17/react")
    #agent = create_react_agent(llm=llm, tools=tools_for_agent, prompt=react_prompt)
    #agent_executor = AgentExecutor(agent = agent, tools=tools_for_agent, verbose = True)

    #result = agent_executor.invoke(
    #    input={"input": prompt_template.format_prompt(message_content=message)}
    #)
    result = llm.invoke(input=prompt_template.format_prompt(message_content=message))

    return result.content


def find_me_jobs():
    global LAST_UPDATE_ID_RECEIVED
    print("Refreshing messages")
    messages = get_telegram_messages(LAST_UPDATE_ID_RECEIVED)
    for message in messages:
        message_obj = message['message']
        LAST_UPDATE_ID_RECEIVED = message['update_id']
        print(f"messages found: {message_obj["text"]}")
        print(is_job_application_message(message_obj["text"]))

schedule.every(5).seconds.do(find_me_jobs)


if __name__=="__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)

