# job-analyzer

## install ollama . Please refer this https://ollama.com/download/linux

## To run ollama run the below commands
# ollama serve
# ollama pull tinyllama
# ollama pull orca-mini

# [tinyllama and orca-mini are small models. Any llm would work]

## To run the Tool
# poetry install
# poetry shell
# uvicorn job_analyzer.job_analyzer_app:app --reload 