# How to deploy to Uberspace U8 / entorb.net

Layout on webserver:

- `~/be/mindchat/` — `src/`, `requirements.txt`, `.streamlit/config.toml` (from `config-prod.toml`), `.streamlit/secrets.toml`
- `~/.config/systemd/user/` — the 3 unit files below

## Deploy

Run `./scripts/deploy.sh` locally: checks, copies code + config, installs packages, stops the app.
Next request starts the new version.

## Service: idle shutdown

Streamlit runs only while used, stops after 1h without open connections (saves RAM).
First request after idle takes ~5s (Streamlit startup).

```txt
:8504 streamlit-mindchat.socket         always listening, starts proxy on first connection
   -> streamlit-mindchat-proxy.service  systemd-socket-proxyd, exits after 1h idle
   -> streamlit-mindchat.service        streamlit on 127.0.0.1:8505, StopWhenUnneeded
```

- [streamlit-mindchat.socket](streamlit-mindchat.socket)
- [streamlit-mindchat-proxy.service](streamlit-mindchat-proxy.service)
- [streamlit-mindchat.service](streamlit-mindchat.service) — `MALLOC_ARENA_MAX=2` limits glibc malloc arenas (less fragmentation from per-session threads)

Open browser tabs keep a websocket open, so the app counts as busy until every tab is closed.

Push unit files (after changing them), run locally:

```sh
./scripts/push.sh
```

```sh
# status
systemctl --user status streamlit-mindchat.socket streamlit-mindchat-proxy streamlit-mindchat
# stop now (next request starts it again)
systemctl --user stop streamlit-mindchat-proxy streamlit-mindchat
# logs
journalctl --user -u streamlit-mindchat -f
# RAM
ps -o rss=,cmd= -C python3.14
```

## Register backend

```sh
uberspace web backend add /mindchat port 8504
uberspace web backend list
```
