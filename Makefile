export DISPLAY := :0
VENV   = venv
PYTHON = $(VENV)/bin/python3
PIP    = $(VENV)/bin/pip
MYPY   = $(VENV)/bin/mypy

install:
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install --upgrade pip setuptools wheel build
	$(PIP) install -r requirements

run:
	$(PYTHON) a_maze_ing.py config.txt

build:
	$(PYTHON) -m build
	mv dist/mazegen-1.0.0-py3-none-any.whl .

debug:
	$(PYTHON) -m pdb a_maze_ing.py config.txt

lint:
	-flake8 . --exclude=$(VENV),mlx
	-$(MYPY) . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs  --exclude $(VENV)

clean:
	rm -rf venv __pycache__ */__pycache__ .mypy_cache */*.mypy_cache maze.txt mazegen.egg-info dist

 .PHONY: install run debug lint clean build