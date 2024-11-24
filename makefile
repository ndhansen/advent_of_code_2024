.PHONY = develop clean

.venv/.venvsetup:
	python3.13 -m venv .venv
	.venv/bin/python3 -m pip install --upgrade pip uv
	.venv/bin/python3 -m uv pip install hatch
	touch $@


.venv/.devsetup: | .venv/.venvsetup
	.venv/bin/python3 -m uv pip install -e .[dev]
	.venv/bin/python3 -m uv pip install -e ../advent_of_code_utils
	touch $@

develop: | .venv/.devsetup

clean:
	rm -rf .venv
