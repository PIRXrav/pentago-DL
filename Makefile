run_test:
	python -m unittest

run_coverage:
	coverage run -m unittest
	coverage report -m
	coverage html

run_pylint:
	find . -type f -name "*.py" | xargs pylint
