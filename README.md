# AI paper digest viewer

Run the existing paper catalog locally with a small Flask-only environment:

```sh
python3 -m venv .venv-viewer
.venv-viewer/bin/python -m pip install 'Flask>=3.1,<4'
bash serve.sh
```

Open http://127.0.0.1:8082. The launcher works from any current directory. It does not run the database refresh or Git publication scripts, or install the PDF/model processing dependencies.

`AI_PAPER_PYTHON` overrides the interpreter. `AI_PAPER_DATA_DIR` overrides the data directory (default: `user_data` beside the server). Use a new directory for isolated experiments; the default directory contains existing tracked data.

`AI_PAPER_HOST` and `AI_PAPER_PORT` override the listener; debug is off unless `AI_PAPER_DEBUG=1`. This prototype has no authentication and is intended for local use.

The frontend loads CDN assets. Browser rendering and paper-content HTML sanitization have not been audited. The refresh and auto-push scripts still contain their original machine-specific paths and remote publication behavior; they are separate from this launcher.
