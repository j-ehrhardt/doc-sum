<a href="https://www.python.org/downloads/release/python-3120/"><img src="https://img.shields.io/badge/Python-3.12-2ea44f" alt="Python - 3.12"></a>
<a href="https://mamba.readthedocs.io/en/latest/installation/mamba-installation.html"><img src="https://img.shields.io/badge/mamba-3.23-green" alt="mamba - 3.23"></a>
<a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue" alt="License - MIT"></a>

# doc-sum

This repository contains a divide and conquer lang-chain script for summarizing large text-corpora with LLMs. 
The script iteratively crawls through a directory of pdfs and feeds them into an instance of a GPT, along with a prompt including questions, topics, or search terms.
The resulting excerpts are buffered in a dictionary and finally summed in a response summary. 
The response is saved in a separate file in the `response` directory. 


# Requirements

All requirements are saved in the `venv.yml` file. 
You can install the python environemnt by typing: 

```bash
mamba env create -f venv.yml 
```
The main dependency is the langchain library. 

# Usage

> [WARNING]
> This script only works, if you acquired tokens from OpenAI. Every use of the script will use tokens from your project's OpenAI account.

1. Save the documents of your corpus as individual documents into the `data` directory.
2. (If necessary: Adapt the model in the `sum_openai.py` file.)

You can run the script either from a jupyter notebook or from the command line. 

When running the script from the command line:

3. Open your terminal and navigate to the `code` directory.
4. activate your mamba environment and type: 
```bash
python  main.py --query '<ENTER-YOUR-QUERY>'
```
5. You can find your answer as separate file in the `responses` directory. The file is named after your query objective. 
6. If you need help, type: 
```bash
python main.py --help
```
 
When running the script from the jupyter notebook: 

5. Open your terminal and activate your mamba environment. 
6. Start your jupyter server, adapt the information in the cells
7. Adapt your queries in the query cells.
8. Run your pipeline cell.
9. You will get the answer as prompt below your cell. Additionally, your answer as separate file in the `responses` directory. The file is named after your query objective. 


# License

The code is licensed under MIT license. 
Refer to the [LICENSE](LICENSE) file for more information.





