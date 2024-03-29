FROM python:3.9.12

RUN pip install poetry
RUN mkdir /app
WORKDIR /app

COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

COPY streamlit-app.py /app/streamlit-app.py
COPY dashboard /app/dashboard
ENV PYTHONPATH=$PWD:$PYTHONPATH

EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "--server.headless", "true", "--server.port", "8501", "streamlit-app.py"]
