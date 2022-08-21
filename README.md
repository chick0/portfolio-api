# portfolio-api

my portfolio api server written with FastAPI

* web client: [chick0/portfolio-client](https://github.com/chick0/portfolio-client)

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
