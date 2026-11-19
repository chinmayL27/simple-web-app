# Interview Practice API

A small Python web API for interview exercises. FastAPI serves the endpoints and SQLAlchemy connects to a SQL database using the `DATABASE_URL` environment variable. SQLite is the default and stores data in `data/app.db`, so no separate database server is needed.

## Requirements

- Python 3.10 or newer
- Windows PowerShell or Command Prompt

## Run on Windows

From this folder, create and activate a virtual environment, install dependencies, and start the server:

```powershell
py -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0
```

If PowerShell blocks activation, run the commands without activating by replacing `python` with `.venv\Scripts\python.exe` and `uvicorn` with `.venv\Scripts\python.exe -m uvicorn`.

Open http://127.0.0.1:8000 in your browser to use the records page, or http://127.0.0.1:8000/docs to explore and call the API interactively. The database and `records` table are created automatically on startup. Set `DATABASE_URL` to connect to another SQL database. Install the matching SQLAlchemy driver for that database.

## Endpoints

- `GET /health` returns `{"status":"ok"}`.
- `POST /records` creates a record. JSON example: `{"name":"Example record","description":"Optional description"}`.
- `GET /records` lists saved records.
- `GET /records/{record_id}` returns one record or a 404 response.

SQLAlchemy uses parameterized SQL for database writes and reads. The server listens on all network interfaces. Open http://127.0.0.1:8000 on this machine. To connect from another device on the same network, use this computer’s local IP address, such as http://192.168.1.20:8000, and allow Python through Windows Firewall for private networks.
