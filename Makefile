docker_build:
	docker build -t eu.gcr.io/census-rm-ci/rm/census-rm-dev-tools .

flake:
	pipenv run flake8

check:
	PIPENV_PYUP_API_KEY="" pipenv check
