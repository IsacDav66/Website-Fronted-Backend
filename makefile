SHELL=/bin/sh

source:
	source ~/envs/certus_back/bin/activate

run:
	pip install -r requirements.txt && \
	python main.py


gcd:
	gcloud app deploy app.yaml \
		--project natural-cistern-400217
