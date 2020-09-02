

# Install pyenv
git clone https://github.com/pyenv/pyenv.git ~/.pyenv
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bashrc
echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bashrc
echo -e 'if command -v pyenv 1>/dev/null 2>&1; then\n  eval "$(pyenv init -)"\nfi' >> ~/.bashrc
source ~/.bashrc

# Install an up to date python 3, pipenv and then create the pipenv for the dev-tools
echo "Installing python 3.8.5, this might take several minutes..."
pyenv install 3.8.5
pyenv global 3.8.5
pip install -U pip pipenv
pipenv install --dev

# Add tools/shortcuts to shell
cat cloudshell_setup/bash_tools.sh >> ~/.bashrc

exec "$SHELL"
