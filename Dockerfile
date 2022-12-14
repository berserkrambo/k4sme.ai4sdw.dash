FROM python:3.9.12

RUN pip install poetry
RUN mkdir /app
WORKDIR /app

COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

COPY dashboard /app/dashboard

ENV PYTHONPATH=$PWD:$PYTHONPATH

EXPOSE 8000
ENTRYPOINT ["streamlit", "run", "dashboard/main.py", "--server.address", "0.0.0.0", "--server.port", "8000"]
