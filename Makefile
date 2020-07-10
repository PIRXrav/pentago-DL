run_test:
	python -m unittest

run_coverage:
	coverage run -m unittest
	coverage report -m
	coverage html
