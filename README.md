# FastAPI-Blog


**Commands for Migrations:**

-   alembic stamp head

-   alembic revision -m "Commit message" --autogenerate

-   alembic upgrade head

-   alembic stamp head


**Commands for starting docker:**

-   docker-compose up --build


**Commands for starting without docker:**

-   uvicorn app.main:app --reload


If Running on Docker, Use host.docker.internal instead of localhost for Database Credentials
