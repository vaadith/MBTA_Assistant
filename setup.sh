# Check if already in a virtual environment
if [[ ! "$VIRTUAL_ENV" ]]; then
    echo "Not in a virtual environment. Creating one..."
    python3 -m venv myenv
    source myenv/bin/activate
fi

# Ensure pip is installed
echo "Ensuring pip is installed..."
python3 -m ensurepip --upgrade

# Install dependencies from requirements.txt using pipenv
echo "Installing dependencies from requirements.txt..."
pip install -r requirements.txt

# Provide information to user
echo "Setup completed."