.PHONY: setup notebook

setup:
	@bin/setup.sh

notebook:
	@( \
		source venv/bin/activate; \
		jupyter notebook \
	)