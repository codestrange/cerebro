run:
	export FLASK_APP=run.py &&\
	export FLASK_ENV=production &&\
	export FLASK_DEBUG=0 &&\
	flask run

run_dev:
	export FLASK_APP=run.py &&\
	export FLASK_ENV=development &&\
	export FLASK_DEBUG=1 &&\
	flask run

shell:
	export FLASK_APP=run.py &&\
	flask shell

test:
	export FLASK_APP=run.py &&\
	flask test
