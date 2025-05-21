#!/usr/bin/env bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add UV to PATH based on where it was installed
if [ -f "$HOME/.cargo/env" ]; then
    . $HOME/.cargo/env
elif [ -f "$HOME/.local/bin/env" ]; then
    . $HOME/.local/bin/env
fi

# Add both possible UV installation locations to PATH
export PATH="$HOME/.cargo/bin:$HOME/.local/bin:$PATH"

# Verify UV is installed
which uv
uv --version

# Install CPU-only PyTorch first
uv pip install torch==2.2.2 torchvision==0.17.2 torchaudio==2.2.2

# Then install the rest of the project
cd project_api
uv pip install -e .