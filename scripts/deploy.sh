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
rsync -uz requirements.txt entorb8@mab.uberspace.de:be/mindchat/

# .streamlit/*.toml
# config.toml -> config-prod.toml
uv run scripts/config_convert.py
rsync -uz .streamlit/config-prod.toml entorb8@mab.uberspace.de:be/mindchat/.streamlit/config.toml
rsync -uz .streamlit/secrets.toml entorb8@mab.uberspace.de:be/mindchat/.streamlit/secrets.toml

# src
rsync -ruzv --no-links --delete --delete-excluded --exclude __pycache__ src/ entorb8@mab.uberspace.de:be/mindchat/src/

# echo installing packages
ssh entorb8@mab.uberspace.de "python3.14 -m pip install --user -r be/mindchat/requirements.txt > /dev/null"

# touch main.py: update time stamp for version info
echo restarting mindchat
ssh entorb8@mab.uberspace.de "touch be/mindchat/src/main.py && systemctl --user restart streamlit-mindchat"

echo DONE
