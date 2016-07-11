
.PHONY: test
test: pep8
	python runtests.py

.PHONY: pep8
pep8:
	@flake8 * --ignore=F403,F401 --exclude=requirements.txt,*.pyc,*.md,Makefile,LICENSE,*.in

.PHONY: sdist
sdist: test
	@python setup.py sdist upload

.PHONY: clean
clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
