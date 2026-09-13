Shuttle Event Processing System

Files:

* shuttle_processor.py - creates events and events.json
* api.py - FastAPI POST /events endpoint
* test.py - automated tests
* events.json - generated event data

Run:

1. Run main code and generate JSON:
   python shuttle_processor.py

3. Run tests:
   python -m pytest test.py -v

Requirements:
pip install pandas fastapi pytest httpx2

Expected tests result:
3 passed
