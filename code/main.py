import argparse
from sum_openai import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--query', required=True, type=str, help='set the query on which you want to compare and sum your corpus.')

    parser.add_argument('--model_name', required=False, type=str, default='gpt-4o-mini', help='set the model you want to work with.')
    parser.add_argument('--system_prompt', required=False, type=str, help='set the system prompt, your model shall be pre-prompted with.')
    parser.add_argument('--crawl_user_prompt', required=False, type=str, help='set the user prompt, your model shall be pre-prompted with while crawling all documents.')
    parser.add_argument('--sum_user_prompt', require=False, type=str, help='set the user prompt, your model shall be pre-prompted with while summing the corpus excerpts')
    args = parser.parse_args()

    # Assign default values if optional arguments are not provided
    defaults = {
        "model_name": "gpt-4o-mini",
        "system_prompt": "You are a helpful assistant that helps me in crawling large pdf corpora, extracting information given the topics and questions you get asked. You do not hallucinate. You are precise, concise and base your summaries only on information you extracted from the documents.",
        "crawl_user_prompt": f"Summarize the main arguments of the given text under the following perspective {args.query}.",
        "sum_user_prompt": f"You are given summaries of multiple documents. The summaries are separated by headlines which indicate the document title. Your task is to extract similarities from the individual summaries and point them out under the perspective of {args.query}. Mark from which document summary you withdrew the information"
    }

    for key, default in defaults.items():
        if getattr(args, key) is None:
            setattr(args, key, default)


    answer_dict, model = crawl_pdfs(data_dir='../data', system_prompt=system_prompt, user_prompt=crawl_user_prompt)
    response = sum_answers(answer_dict=answer_dict, model=model, system_prompt=system_prompt, user_prompt=sum_user_prompt)
    summary_to_file(response=response, query_objective=query_objective)
