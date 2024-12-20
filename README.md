# doc_sum

This repository contains a lang-chain script for searching and summing large corpora iteratively document per document.
The script iteratively crawls thorugh a directory of pdfs and feeds them into an instance of GPT, along a prompt including questions, topics, or search terms. 
The resulting excerpts are buffered and compared by a final query to GPT. 

# Requirements

All requirements are saved in the `venv.yml` file. 
You can install the python environemnt by typing: 

```bash
mamba env create -f venv.yml 
```
The main dependency is the langchain library. 

# Usage




