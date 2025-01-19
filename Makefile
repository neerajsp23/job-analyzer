.PHONY run_app

run_app:
	uvicorn job_analyzer.job_analyzer_app:app --reload