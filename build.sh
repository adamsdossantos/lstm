#!/usr/bin/env bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add UV to PATH
export PATH="$HOME/.cargo/bin:$PATH"

# Activate UV environment
. $HOME/.cargo/env

# Install project using UV and pyproject.toml
cd project_api
uv pip install -e .