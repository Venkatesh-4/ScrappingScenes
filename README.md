pip freeze > requirements.txt
pip install -r requirements.txt
playwright install
python -m backend.database.create_tables
python -m backend.scraper.fetcher
uvicorn backend.api.server:app --reload
