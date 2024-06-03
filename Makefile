init:
	python3.9 -m venv venv
	. venv/bin/activate; pip install --upgrade pip
	. venv/bin/activate; pip install -r requirements.txt

start:
	. venv/bin/activate; export PYTHONPATH='.'; python manage.py runserver
