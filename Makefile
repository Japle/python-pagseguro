.PHONY: test
test: pep8
	py.test --cov-report term-missing --cov pagseguro

.PHONY: pep8
pep8:
	@flake8 * --ignore=F403,F401 --exclude=requirements.txt,requirements_dev.txt,*.pyc,*.md,Makefile,LICENSE,*.in

.PHONY: publish
publish: test
	@python setup.py sdist upload

.PHONY: clean-pyc clean-build clean
clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info
	rm -fr *.egg

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +
