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

### string to gpt ###

def init_env():
    if not os.environ.get('OPENAI_API_KEY'):
        os.environ['OPENAI_API_KEY'] = getpass.getuser('Enter API key for OpenAI:   ')

    model = ChatOpenAI(model='gpt-4o-mini')
    return model


def query_model(pre_prompt, main_prompt, model):
    query = [
        SystemMessage(pre_prompt),
        HumanMessage(main_prompt)
    ]

    response = model.invoke(query)
    return response

### iterate through docs ###

def crawl_pdfs(data_dir, pre_prompt, main_prompt):
    model = init_env()
    doc_list = os.listdir(data_dir)

    answer_dict = {}
    for doc in doc_list:
        if doc[-3:] == 'pdf':
            text = pdf_to_string(os.path.join(data_dir, doc))
            prompt = main_prompt + ' ' + text
            response = query_model(pre_prompt, main_prompt, model)

            answer_dict[doc] = response
    return answer_dict


def sum_answers(answer_dict):
    pre_prompt = ''
    main_prompt = ''



    return




if __name__ == '__main__':
    pre_prompt = 'You are a helpful assistant that helps me in crawling large pdf corpora, extracting information given the topics and questions you get asked.'
    main_prompt = 'Summarize the main points of the given text'

    crawl_pdfs(data_dir='../data', pre_prompt=pre_prompt, main_prompt=main_prompt)