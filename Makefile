VENV   = venv
PYTHON = $(VENV)/bin/python3
PIP    = $(VENV)/bin/pip
MLX = /mlx/mlx.py


install:
	python3 -m venv $(VENV)
	$(PYTHON) -m pip install --upgrade pip
	$(PIP) install -r ./utils/requirements

run:
	$(PYTHON) a_maze_ing.py config.txt

debug:
	$(PYTHON) -m pdb a_maze_ing.py config.txt

lint:
	flake8 . --exclude=$(MLX)$(VENV)
	mypy . --warn-return-any --warn-unused-ignores --ignore-missing-imports --disallow-untyped-defs --check-untyped-defs --exclude $(VENV)

clean:
	rm -rf venv __pycache__ */__pycache__ .mypy_cache */*.mypy_cache maze.txt