#!/bin/sh
cd $(dirname $0)/..

echo copying
# requirements
uv run scripts/gen_requirements.py
rsync -uz requirements.txt entorb@entorb.net:streamlit-mindchat/

# .streamlit/*.toml
# config.toml -> config-prod.toml
uv run scripts/config_convert.py
rsync -uz .streamlit/config-prod.toml entorb@entorb.net:streamlit-mindchat/.streamlit/config.toml
rsync -uz .streamlit/secrets.toml entorb@entorb.net:streamlit-mindchat/.streamlit/secrets.toml

# src
rsync -ruzv --no-links --delete --delete-excluded --exclude __pycache__ src/ entorb@entorb.net:streamlit-mindchat/src/

# echo installing packages
ssh entorb@entorb.net "pip3.11 install --user -r streamlit-mindchat/requirements.txt > /dev/null"

echo restarting streamlit-mindchat
ssh entorb@entorb.net "supervisorctl restart streamlit-mindchat"
