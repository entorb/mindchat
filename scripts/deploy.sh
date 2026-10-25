#!/bin/sh
set -e
cd "$(dirname "$0")/.."

# cleanup
rm -f .DS_Store
rm -f -- ./*/.DS_Store

# spelling
sh scripts/run_spelling.sh

# ruff
sh scripts/run_ruff.sh
sh scripts/run_pytest.sh

echo copying
# requirements
uv run scripts/gen_requirements.py
rsync -uz requirements.txt entorb@entorb.net:be/mindchat/

# .streamlit/*.toml
# config.toml -> config-prod.toml
uv run scripts/config_convert.py
rsync -uz .streamlit/config-prod.toml entorb@entorb.net:be/mindchat/.streamlit/config.toml
rsync -uz .streamlit/secrets.toml entorb@entorb.net:be/mindchat/.streamlit/secrets.toml

# src
rsync -ruzv --no-links --delete --delete-excluded --exclude __pycache__ src/ entorb@entorb.net:be/mindchat/src/

# echo installing packages
ssh entorb@entorb.net "pip3.11 install --user -r be/mindchat/requirements.txt > /dev/null"

# touch main.py: update time stamp for version info
echo restarting mindchat
ssh entorb@entorb.net "touch be/mindchat/src/main.py && supervisorctl restart streamlit-mindchat"

echo DONE
