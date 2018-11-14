# Project configuration
PROJECT_NAME = python-tplink-smarthome
PACKAGE_NAME = tplink_smarthome
TESTS_DIRECTORY = tests

# Call these functions before/after each target to maintain a coherent display
START_TARGET = @printf "[$(shell date +"%H:%M:%S")] %-40s" "$(1)"
END_TARGET = @printf "\033[32;1mOK\033[0m\n"

# Parameter expansion
PYTEST_OPTS ?=

ENV_RUN =

.PHONY: help check_code_style check_doc_style check_pylint check_xenon \
        check_lint check_test check distclean clean doc dist \
        ci_env ci_check ci_doc

help: ## Display list of targets and their documentation
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk \
		'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

doc: ## Build documentation
	$(call START_TARGET,Generating documentation)
	@$(ENV_RUN) make -C doc html
	$(call END_TARGET)

check_code_style: ## Check code style
	$(call START_TARGET,Checking code style)
	@$(ENV_RUN) pycodestyle $(PACKAGE_NAME) $(TESTS_DIRECTORY)
	$(call END_TARGET)

check_doc_style: ## Check documentation style
	$(call START_TARGET,Checking doc style)
	@$(ENV_RUN) pydocstyle $(PACKAGE_NAME) $(TESTS_DIRECTORY)
	$(call END_TARGET)

check_pylint: ## Run pylint
	$(call START_TARGET,Checking pylint)
	@$(ENV_RUN) pylint --reports=no --jobs=2 $(PACKAGE_NAME) $(TESTS_DIRECTORY)
	$(call END_TARGET)

check_xenon: ## Run xenon (code complexity)
	$(call START_TARGET,Checking xenon)
	@$(ENV_RUN) xenon $(PACKAGE_NAME) --no-assert
	$(call END_TARGET)

check_lint: check_code_style check_doc_style check_pylint check_xenon ## Check code style, documentation style, pylint and xenon

check_test: ## Run py.test
	$(call START_TARGET,Checking $(TESTS_DIRECTORY))
	@$(ENV_RUN) py.test --cov=$(PACKAGE_NAME) --cov-fail-under=0 --duration=10 $(PYTEST_OPTS) $(TESTS_DIRECTORY)
	$(call END_TARGET)

check: check_lint check_test ## Run all checks (lint and tests)

distclean: clean ## Remove *.egg-info and apply clean
	$(call START_TARGET,Distribution cleaning)
	@rm -rf *.egg-info
	$(call END_TARGET)

clean: ## Remove temporary and build files
	$(call START_TARGET,Cleaning)
	@find . -type f -name '*.pyc' -delete
	@rm -rf dist/* .cache .eggs
	@rm -rf htmlcov .coverage
	@rm -rf doc/source/api
	@$(ENV_RUN) make -C doc clean
	$(call END_TARGET)

dist: ## Create a source distribution
	$(call START_TARGET,Creating distribution)
	@$(ENV_RUN) python setup.py --quiet sdist --dist-dir _tmp_dist
	@mkdir -p dist
	@mv _tmp_dist/*.tar.gz dist/$(PROJECT_NAME)-$$(git describe --always).tar.gz
	@rm -rf _tmp_dist
	$(call END_TARGET)

ci_env: ## Build a CI environment
	virtualenv ${CURDIR}/ci_env
	${CURDIR}/ci_env/bin/pip install -U pip
	${CURDIR}/ci_env/bin/pip install -r ${CURDIR}/requirements/development.txt
	${CURDIR}/ci_env/bin/pip install -e ${CURDIR}

ci_check: ci_env ## Run all checks in the CI environment
	bash -c "source ${CURDIR}/ci_env/bin/activate && \
		$(MAKE) -f Makefile check \
		PYTEST_OPTS='-vv --junit-xml=junit.xml --cov $(PACKAGE_NAME) --cov-report xml:cov.xml'"
	bash -c "source ${CURDIR}/ci_env/bin/activate && \
		cobertura-clover-transform ${CURDIR}/cov.xml -o ${CURDIR}/clover.xml"

ci_doc: ci_env ## Build the documentation in the CI environment
	bash -c "source ${CURDIR}/ci_env/bin/activate && $(MAKE) -f Makefile doc"
