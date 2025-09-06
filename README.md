# FastAPI + SQLAlchemy Demo Application

A small but clean FastAPI project I made whilst learning web development and object relational mapping, demonstrating a layered architecture:

- **Routers/Endpoints** (FastAPI)  
- **Services** (business logic)  
- **Repositories** (data access / CRUD)  
- **SQLAlchemy ORM models** (with a many-to-many between customers and shows, and a many-to-one from shows to an *avanue*)  

The code intentionally keeps things straightforward while still showing good patterns (generic repository, service layer, dependency injection for DB sessions).


## Tech stack
- **FastAPI** for the web API  
- **SQLAlchemy 2.x** ORM  
- **Pydantic v2** for request/response models  
- **Uvicorn** as the ASGI server  
- **python-dotenv** for environment variables  

