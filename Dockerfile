FROM python:3.9.12

RUN pip install poetry
RUN mkdir /app
WORKDIR /app

COPY poetry.lock pyproject.toml /app/
RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

COPY dashboard /app/dazzler

ENV PYTHONPATH=$PWD:$PYTHONPATH

EXPOSE 8081
ENTRYPOINT ["streamlit", "run", "dazzler/main_st.py", "--server.address", "0.0.0.0", "--server.port", "8081"]
