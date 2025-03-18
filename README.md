pip freeze > requirements.txt
pip install -r requirements.txt
playwright install
uvicorn backend.api.server:app --reload
