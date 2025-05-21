#!/usr/bin/env bash
# Add both possible UV installation locations to PATH
export PATH="$HOME/.cargo/bin:$HOME/.local/bin:$PATH"

# Activate the environment if available
if [ -f "$HOME/.cargo/env" ]; then
    . $HOME/.cargo/env
elif [ -f "$HOME/.local/bin/env" ]; then
    . $HOME/.local/bin/env
fi

# Run the API (adjust the file name if needed)
cd project_api
python main.py