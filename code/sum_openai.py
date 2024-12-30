import os
import json
import getpass
import argparse

from PyPDF2 import PdfReader
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage


### pdf to string ###

def pdf_to_string(file_path):
    reader = PdfReader(file_path)
    text = '\n'.join([page.extract_text() for page in reader.pages])
    return text


### string to llm ###

def init_env():
    if not os.environ.get('OPENAI_API_KEY'):
        os.environ['OPENAI_API_KEY'] = getpass.getuser('Enter API key for OpenAI:   ')
        # os.environ['OPENAI_API_SECRET'] = '<ENTER-YOUR-KEY-HERE>'

    model = ChatOpenAI(model='gpt-4o-mini')
    return model


def query_model(system_prompt, user_prompt, model):
    query = [
        SystemMessage(system_prompt),
        HumanMessage(user_prompt)
    ]

    response = model.invoke(query)
    return response


### iterate through corpus ###

def crawl_pdfs(data_dir, system_prompt, user_prompt):
    model = init_env()
    doc_list = os.listdir(data_dir)

    answer_dict = {}
    for doc in doc_list:
        if doc[-3:] == 'pdf':
            text = pdf_to_string(os.path.join(data_dir, doc))
            prompt = user_prompt + ' ' + text
            response = query_model(system_prompt, user_prompt, model)

            answer_dict[doc] = response
    return answer_dict, model


### sum answers ###

def sum_answers(answer_dict, model, system_prompt, user_prompt):
    input = ''
    for key in answer_dict:
        input += f'# {key} \n\n {answer_dict[key]}'

    prompt = user_prompt + ' ' + input
    response = query_model(system_prompt=system_prompt, user_prompt=prompt, model=model)
    return response


### save answer in file ###

def summary_to_file(response, query_objective):
    save_path = '../responses'

    with open(os.path.join(save_path, query_objective), 'w') as f:
        f.write(response)

    print(f'Summary saved to {os.path.join(save_path, query_objective)}')




if __name__ == '__main__':
    query_objective = ''

    system_prompt = (f'You are a helpful assistant that helps me in crawling large pdf corpora, extracting information given the topics and questions you get asked. '
                     f'You do not hallucinate. You are precise, concise and base your summaries only on information you extracted from the documents.')

    crawl_user_prompt = f'Summarize the main arguments of the given text under the following perspective {query_objective}.'

    sum_user_prompt = (f'You are given summaries of multiple documents. The summaries are separated by headlines which indicate the document title. '
                       f'Your task is to extract similarities from the individual summaries and point them out under the perspective of {query_objective}. '
                       f'Mark from which document summary you withdrew the information')


    answer_dict, model = crawl_pdfs(data_dir='../data', system_prompt=system_prompt, user_prompt=crawl_user_prompt)
    response = sum_answers(answer_dict=answer_dict, model=model, system_prompt=system_prompt, user_prompt=sum_user_prompt)
    summary_to_file(response=response, query_objective=query_objective)




