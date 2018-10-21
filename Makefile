.PHONY: setup notebook guard

guard-%:
	@if [ "${${*}}" = "" ]; then echo "Environment variable $* not set"; exit 1; fi

setup:
	@bin/setup.sh

notebook:
	@( \
		source venv/bin/activate; \
		jupyter notebook \
	)

output: guard-notebook
output: guard-output
render:
	@( \
		source venv/bin/activate; \
		jupyter nbconvert --to markdown ${notebook} --output ${output} \
	)