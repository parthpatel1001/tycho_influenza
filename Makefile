.PHONY: setup

setup:
	@bin/setup.sh


parse_data:
	@( \
       source venv/bin/activate; \
       python3 src/parse_data.py data/US/US.6142004.csv \
    )