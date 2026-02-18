
setup:
	python -m venv venv
	./venv/bin/pip install -r requirements.txt

analysis:
	python analysis/download_data.py

run:
	python webapp/manage.py runserver

test:
	pytest
