clean-test: ## Remove test and coverage artifacts (e.g., .tox, .coverage)
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/
	rm -fr .pytest_cache

check-pipenv: ## Check that pipenv has been installed
	@if ! command -v pipenv 1> /dev/null 2>&1; \
	then \
		echo "Installing pipenv..."; \
		python -mpip install pipenv; \
		echo "... pipenv installed"; \
	fi
	@if ! command -v pipenv 1> /dev/null 2>&1; \
	then \
		echo "Error - pipenv cannot be installed"; \
		exit 1; \
	fi

clean-venv: check-pipenv ## Remove any install Python virtual environment
	pipenv --rm || echo "No virtualenv has been created yet; that is all good"
	\rm -f Pipfile.lock

test: check-pipenv clean-test
	pipenv run python3 -m pytest tests/ -v $*

install-dependencies: clean-venv ## Install Python dependencies thanks to pipenv
	pipenv install -r requirements.txt --dev

code_style:
	black src/ tests/ *.py
	isort src/ tests/ *.py
