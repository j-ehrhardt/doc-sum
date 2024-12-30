import os
import getpass

from PyPDF2 import PdfReader
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage


### pdf to string ###

def pdf_to_string(file_path):
    reader = PdfReader(file_path)
    text = '\n'.join([page.extract_text() for page in reader.pages])
    return text


### string to llm ###

def init_env(model_name):
    if not os.environ.get('OPENAI_API_KEY'):
        #os.environ['OPENAI_API_KEY'] = getpass.getuser('Enter API key for OpenAI:   ')
        os.environ['OPENAI_API_KEY'] = '<ENTER-YOUR-KEY-HERE>'

    model = ChatOpenAI(model=model_name)
    return model


def query_model(system_prompt, user_prompt, model):
    query = [
        SystemMessage(system_prompt),
        HumanMessage(user_prompt)
    ]

    response = model.invoke(query)
    return response


### iterate through corpus ###

def crawl_pdfs(data_dir, system_prompt, user_prompt, model_name='gpt-4o-mini'):
    model = init_env(model_name=model_name)
    doc_list = os.listdir(data_dir)

    answer_dict = {}
    for doc in doc_list:
        if doc[-3:] == 'pdf':
            text = pdf_to_string(os.path.join(data_dir, doc))
            prompt = user_prompt + ' ' + text
            response = query_model(system_prompt, prompt, model)

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
    # This string contains your main query objective that you want to compare the individual documents on
    query_objective = '<ENTER-YOUR-QUERY-OBJECTIVE-HERE>'

    # The system_prompt pre-prompts the GPT instance
    system_prompt = (f'You are a helpful assistant that helps me in crawling large pdf corpora, extracting information given the topics and questions you get asked. '
                     f'You do not hallucinate. You are precise, concise and base your summaries only on information you extracted from the documents.')

    # This user prompt defines the task of extracting the information from the individual documents
    crawl_user_prompt = f'Summarize the main arguments of the given text under the following perspective {query_objective}.'

    # This user prompt defines the task of summarizing the individual document excerpts
    sum_user_prompt = (f'You are given summaries of multiple documents. The summaries are separated by headlines which indicate the document title. '
                       f'Your task is to extract similarities from the individual summaries and point them out under the perspective of {query_objective}. '
                       f'Mark from which document summary you withdrew the information')


    answer_dict, model = crawl_pdfs(data_dir='../data', system_prompt=system_prompt, user_prompt=crawl_user_prompt)
    response = sum_answers(answer_dict=answer_dict, model=model, system_prompt=system_prompt, user_prompt=sum_user_prompt)
    summary_to_file(response=response, query_objective=query_objective)




