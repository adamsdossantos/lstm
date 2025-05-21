#!/usr/bin/env bash
# Add UV to PATH
export PATH="$HOME/.cargo/bin:$PATH"

# Activate the environment
. $HOME/.cargo/env

# Run the API (adjust the file name if needed)
cd project_api
python main.py