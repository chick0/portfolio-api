# mypt api

**my** **p**or**t**folio **api** written with FastAPI

* svelte client: [chick0/ch1ck.xyz](https://github.com/chick0/ch1ck.xyz)

## how to run

1. (optional) set up venv
   ```
   python -m venv venv
   source venv/bin/activate
   ```
2. install requirements
   ```
   pip install -r requirements.txt
   ```
3. set up dotenv value
   ```
   cp .env.example .env
   vim .env
   ```
4. start uvicorn server
   ```
   ./start.py
   ```
   * add `--no-docs` to disable openapi docs ui
