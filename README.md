# Water Bucket Puzzle (catalog #523)

Al Sweigart — *The Big Book of Small Python Projects*, Project #81.

| Artifact | Path |
|----------|------|
| Book steps | [`BOOK_DIRECTIONS.md`](./BOOK_DIRECTIONS.md) |
| Terminal script | [`reference/waterbucket.py`](./reference/waterbucket.py) |
| Shared logic | [`water_bucket_core.py`](./water_bucket_core.py) |
| Web (FastAPI) | [`web/`](./web/) — port **3007** |

## Run the web demo

```powershell
Set-Location "c:\Users\emmak\Desktop\Content\CodingProjects\PortProjects\demos\water-bucket-puzzle\web"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn main:app --reload --port 3007
```

Open [http://127.0.0.1:3007/](http://127.0.0.1:3007/).

## Run the terminal reference

```powershell
Set-Location "c:\Users\emmak\Desktop\Content\CodingProjects\PortProjects\demos\water-bucket-puzzle"
python reference\waterbucket.py
```
