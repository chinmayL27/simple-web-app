# Interview Practice API

A small Python web API for interview exercises. FastAPI serves the endpoints and SQLite stores data in a local `data/app.db` file. No separate database server is needed.

## Requirements

- Python 3.10 or newer
- Windows PowerShell or Command Prompt

## Run on Windows

From this folder, create and activate a virtual environment, install dependencies, and start the server:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

If PowerShell blocks activation, run the commands without activating by replacing `python` with `.venv\Scripts\python.exe` and `uvicorn` with `.venv\Scripts\python.exe -m uvicorn`.

Open http://127.0.0.1:8000/docs to explore and call the API interactively. The database and `items` table are created automatically on startup. Set `DATABASE_PATH` to use a different SQLite file.

## Endpoints

- `GET /health` returns `{"status":"ok"}`.
- `POST /items` creates an item. JSON example: `{"name":"Web server","description":"Production host"}`.
- `GET /items` lists saved items.
- `GET /items/{item_id}` returns one item or a 404 response.

SQLite uses parameterized SQL for database writes and reads. The app binds to localhost by default through Uvicorn, so it is available to the local machine.
