brew install pyenv
pyenv local 3.10.6
python -m venv .venv

python -m pip install --upgrade pip
pip install -r requirements.txt
pip freeze > requirements.txt